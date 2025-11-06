#!/usr/bin/env python3
"""
PyTools v2.0.0 - Utilities Module
Various utility tools including temp email, QR codes, encoders, etc.
"""

import os
import sys
import time
import base64
import json
import requests
from typing import Optional, Dict, List, Any

from core.base import BaseModule, SystemInfo
from core.utils import get_logger, get_config
from ui.display import Display


class TempEmailModule(BaseModule):
    """Generate and monitor temporary email addresses"""

    def __init__(self, display: Display):
        super().__init__(
            name="Temporary Email",
            description="Generate disposable email addresses",
            category="utilities",
        )
        self.display = display
        self.icon = "📧"

    def execute(self) -> bool:
        try:
            self.display.show_info("Generating temporary email address...")

            # Generate random email
            response = requests.get(
                "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1",
                timeout=10,
            )

            if response.status_code != 200:
                self.display.show_error("Failed to generate email")
                return False

            email_address = response.json()[0]

            self.display.console.print()
            self.display.show_success(f"Temporary Email: {email_address}")
            self.display.console.print()
            self.display.show_info("Checking for emails every 5 seconds...")
            self.display.show_warning("Press Ctrl+C to stop and return to menu")
            self.display.console.print()

            displayed_ids = set()
            login, domain = email_address.split("@")

            try:
                while True:
                    # Check for emails
                    check_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
                    response = requests.get(check_url, timeout=10)

                    if response.status_code == 200:
                        emails = response.json()

                        for email in emails:
                            email_id = email["id"]

                            if email_id not in displayed_ids:
                                # Get full email content
                                read_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={email_id}"
                                email_response = requests.get(read_url, timeout=10)

                                if email_response.status_code == 200:
                                    email_data = email_response.json()

                                    self.display.console.print()
                                    self.display.show_section("📨 New Email Received!")

                                    info = {
                                        "From": email_data.get("from", "Unknown"),
                                        "Subject": email_data.get(
                                            "subject", "No Subject"
                                        ),
                                        "Date": email_data.get("date", "Unknown"),
                                    }

                                    self.display.show_key_value(info, "Email Details")

                                    self.display.console.print()
                                    self.display.console.print("[cyan]Body:[/cyan]")
                                    body = email_data.get(
                                        "textBody",
                                        email_data.get("htmlBody", "No content"),
                                    )
                                    self.display.console.print(body[:500])
                                    if len(body) > 500:
                                        self.display.console.print(
                                            "[dim]...(truncated)[/dim]"
                                        )
                                    self.display.console.print()

                                    displayed_ids.add(email_id)

                    time.sleep(5)

            except KeyboardInterrupt:
                self.display.console.print()
                self.display.show_info("Stopping email monitoring...")
                return True

        except Exception as e:
            self.log_error("Temp email failed", e)
            self.display.show_error(f"Temporary email failed: {str(e)}")
            return False


class QRCodeGeneratorModule(BaseModule):
    """Generate QR codes from text or URLs"""

    def __init__(self, display: Display):
        super().__init__(
            name="QR Code Generator",
            description="Generate QR codes from text or URLs",
            category="utilities",
        )
        self.display = display
        self.icon = "📱"

    def execute(self) -> bool:
        try:
            # Check if qrcode is available
            try:
                import qrcode
            except ImportError:
                self.display.show_error("qrcode module not installed")
                self.display.show_info("Install with: pip install qrcode[pil]")
                return False

            text = self.display.prompt("Enter text or URL for QR code")

            if not text:
                self.display.show_warning("No text provided")
                return False

            filename = self.display.prompt("Output filename", default="qrcode.png")

            self.display.console.print()
            self.display.show_info("Generating QR code...")

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)

            self.display.show_success(f"QR code saved: {filename}")

            # Try to display in terminal
            self.display.console.print()
            self.display.show_info("ASCII representation:")
            self.display.console.print()

            # Print ASCII QR code
            matrix = qr.get_matrix()
            for row in matrix:
                line = ""
                for cell in row:
                    line += "██" if cell else "  "
                self.display.console.print(line)

            return True

        except Exception as e:
            self.log_error("QR code generation failed", e)
            self.display.show_error(f"QR generation failed: {str(e)}")
            return False


class TextEncoderModule(BaseModule):
    """Encode/decode text in various formats"""

    def __init__(self, display: Display):
        super().__init__(
            name="Text Encoder/Decoder",
            description="Encode/decode Base64, Hex, URL encoding",
            category="utilities",
        )
        self.display = display
        self.icon = "🔤"

    def execute(self) -> bool:
        try:
            self.display.console.print("1. Base64 Encode")
            self.display.console.print("2. Base64 Decode")
            self.display.console.print("3. Hex Encode")
            self.display.console.print("4. Hex Decode")
            self.display.console.print("5. URL Encode")
            self.display.console.print("6. URL Decode")
            self.display.console.print()

            choice = self.display.prompt("Choose option", default="1")

            text = self.display.prompt("Enter text")
            if not text:
                self.display.show_warning("No text provided")
                return False

            self.display.console.print()

            try:
                if choice == "1":
                    result = base64.b64encode(text.encode()).decode()
                    self.display.show_info(f"Base64 Encoded: {result}")
                elif choice == "2":
                    result = base64.b64decode(text).decode()
                    self.display.show_info(f"Base64 Decoded: {result}")
                elif choice == "3":
                    result = text.encode().hex()
                    self.display.show_info(f"Hex Encoded: {result}")
                elif choice == "4":
                    result = bytes.fromhex(text).decode()
                    self.display.show_info(f"Hex Decoded: {result}")
                elif choice == "5":
                    import urllib.parse

                    result = urllib.parse.quote(text)
                    self.display.show_info(f"URL Encoded: {result}")
                elif choice == "6":
                    import urllib.parse

                    result = urllib.parse.unquote(text)
                    self.display.show_info(f"URL Decoded: {result}")
                else:
                    self.display.show_warning("Invalid choice")
                    return False

                return True

            except Exception as e:
                self.display.show_error(f"Encoding/decoding failed: {str(e)}")
                return False

        except Exception as e:
            self.log_error("Text encoding failed", e)
            self.display.show_error(f"Text encoding failed: {str(e)}")
            return False


class JSONFormatterModule(BaseModule):
    """Format and validate JSON/YAML"""

    def __init__(self, display: Display):
        super().__init__(
            name="JSON/YAML Formatter",
            description="Format, validate and convert JSON/YAML",
            category="utilities",
        )
        self.display = display
        self.icon = "📄"

    def execute(self) -> bool:
        try:
            self.display.console.print("1. Format JSON")
            self.display.console.print("2. Validate JSON")
            self.display.console.print("3. Minify JSON")
            self.display.console.print("4. JSON to YAML")
            self.display.console.print()

            choice = self.display.prompt("Choose option", default="1")

            self.display.console.print()
            self.display.show_info("Enter JSON (empty line to finish):")

            lines = []
            while True:
                try:
                    line = input()
                    if not line:
                        break
                    lines.append(line)
                except EOFError:
                    break

            json_str = "\n".join(lines)

            if not json_str.strip():
                self.display.show_warning("No JSON provided")
                return False

            self.display.console.print()

            try:
                data = json.loads(json_str)

                if choice == "1":
                    # Format JSON
                    formatted = json.dumps(data, indent=2, sort_keys=True)
                    self.display.show_section("Formatted JSON")
                    self.display.console.print(formatted)

                elif choice == "2":
                    # Validate JSON
                    self.display.show_success("✓ Valid JSON")
                    self.display.show_info(
                        f"Keys: {len(data) if isinstance(data, dict) else 'N/A'}"
                    )

                elif choice == "3":
                    # Minify JSON
                    minified = json.dumps(data, separators=(",", ":"))
                    self.display.show_section("Minified JSON")
                    self.display.console.print(minified)

                elif choice == "4":
                    # JSON to YAML
                    try:
                        import yaml

                        yaml_str = yaml.dump(data, default_flow_style=False)
                        self.display.show_section("YAML")
                        self.display.console.print(yaml_str)
                    except ImportError:
                        self.display.show_error("PyYAML not installed")
                        self.display.show_info("Install with: pip install pyyaml")
                        return False
                else:
                    self.display.show_warning("Invalid choice")
                    return False

                return True

            except json.JSONDecodeError as e:
                self.display.show_error(f"Invalid JSON: {str(e)}")
                return False

        except Exception as e:
            self.log_error("JSON formatting failed", e)
            self.display.show_error(f"JSON formatting failed: {str(e)}")
            return False


class UUIDGeneratorModule(BaseModule):
    """Generate UUIDs"""

    def __init__(self, display: Display):
        super().__init__(
            name="UUID Generator",
            description="Generate unique identifiers (UUIDs)",
            category="utilities",
        )
        self.display = display
        self.icon = "🆔"

    def execute(self) -> bool:
        try:
            import uuid

            count_str = self.display.prompt("Number of UUIDs to generate", default="5")
            try:
                count = int(count_str)
                count = max(1, min(count, 50))
            except:
                count = 5

            self.display.console.print()
            self.display.show_section("🆔 Generated UUIDs")

            for i in range(count):
                uid = str(uuid.uuid4())
                self.display.console.print(f"  {i + 1}. [green]{uid}[/green]")

            return True

        except Exception as e:
            self.log_error("UUID generation failed", e)
            self.display.show_error(f"UUID generation failed: {str(e)}")
            return False


def get_utility_modules(display: Display) -> List[BaseModule]:
    """Get all utility modules"""
    return [
        TempEmailModule(display),
        QRCodeGeneratorModule(display),
        TextEncoderModule(display),
        JSONFormatterModule(display),
        UUIDGeneratorModule(display),
    ]
