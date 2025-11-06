#!/usr/bin/env python3
"""
PyTools v2.0.0 - Security Module
Security analysis, password tools, and protection utilities
"""

import os
import re
import secrets
import string
import hashlib
from typing import Optional, Dict, List, Any

from core.base import BaseModule, SystemInfo, CommandExecutor
from core.utils import get_logger, get_config
from ui.display import Display


class PasswordStrengthModule(BaseModule):
    """Check password strength"""

    def __init__(self, display: Display):
        super().__init__(
            name="Check Password Strength",
            description="Analyze password strength and security",
            category="security",
        )
        self.display = display
        self.icon = "🔐"

    def execute(self) -> bool:
        try:
            password = self.display.prompt(
                "Enter password to check strength", password=True
            )

            if not password:
                self.display.show_warning("No password provided")
                return False

            self.display.console.print()

            # Analyze password
            analysis = self._analyze_password(password)

            # Display results
            strength = analysis["strength"]
            score = analysis["score"]
            color = analysis["color"]

            self.display.console.print(
                f"[{color}]Password Strength: {strength} ({score}/100)[/{color}]"
            )
            self.display.console.print()

            # Show details
            details = {
                "Length": str(analysis["length"]),
                "Has Uppercase": "✓" if analysis["has_upper"] else "✗",
                "Has Lowercase": "✓" if analysis["has_lower"] else "✗",
                "Has Numbers": "✓" if analysis["has_digit"] else "✗",
                "Has Special Chars": "✓" if analysis["has_special"] else "✗",
                "Estimated Crack Time": analysis["crack_time"],
            }

            self.display.show_key_value(details, "🔐 Password Analysis")

            # Show recommendations
            if analysis["recommendations"]:
                self.display.console.print()
                self.display.show_section("💡 Recommendations")
                for rec in analysis["recommendations"]:
                    self.display.console.print(f"  • {rec}")

            return True

        except Exception as e:
            self.log_error("Password check failed", e)
            self.display.show_error(f"Failed to check password: {str(e)}")
            return False

    def _analyze_password(self, password: str) -> Dict[str, Any]:
        """Analyze password strength"""
        length = len(password)
        has_upper = bool(re.search(r"[A-Z]", password))
        has_lower = bool(re.search(r"[a-z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

        # Calculate score
        score = 0
        if length >= 8:
            score += 20
        if length >= 12:
            score += 15
        if length >= 16:
            score += 15
        if has_upper:
            score += 15
        if has_lower:
            score += 15
        if has_digit:
            score += 10
        if has_special:
            score += 10

        # Determine strength
        if score >= 90:
            strength = "Very Strong"
            color = "bright_green"
            crack_time = "Centuries+"
        elif score >= 70:
            strength = "Strong"
            color = "green"
            crack_time = "Years to decades"
        elif score >= 50:
            strength = "Medium"
            color = "yellow"
            crack_time = "Days to months"
        elif score >= 30:
            strength = "Weak"
            color = "orange"
            crack_time = "Hours to days"
        else:
            strength = "Very Weak"
            color = "red"
            crack_time = "Minutes to hours"

        # Generate recommendations
        recommendations = []
        if length < 12:
            recommendations.append("Use at least 12 characters")
        if not has_upper:
            recommendations.append("Add uppercase letters (A-Z)")
        if not has_lower:
            recommendations.append("Add lowercase letters (a-z)")
        if not has_digit:
            recommendations.append("Add numbers (0-9)")
        if not has_special:
            recommendations.append("Add special characters (!@#$%^&*)")

        return {
            "strength": strength,
            "score": score,
            "color": color,
            "length": length,
            "has_upper": has_upper,
            "has_lower": has_lower,
            "has_digit": has_digit,
            "has_special": has_special,
            "crack_time": crack_time,
            "recommendations": recommendations,
        }


class PasswordGeneratorModule(BaseModule):
    """Generate secure random passwords"""

    def __init__(self, display: Display):
        super().__init__(
            name="Password Generator",
            description="Generate secure random passwords",
            category="security",
        )
        self.display = display
        self.icon = "🔑"

    def execute(self) -> bool:
        try:
            # Get preferences
            length_str = self.display.prompt("Password length", default="16")
            try:
                length = int(length_str)
                if length < 8:
                    self.display.show_warning("Minimum length is 8, using 8")
                    length = 8
                elif length > 128:
                    self.display.show_warning("Maximum length is 128, using 128")
                    length = 128
            except:
                length = 16

            use_special = self.display.confirm(
                "Include special characters?", default=True
            )
            count_str = self.display.prompt(
                "Number of passwords to generate", default="5"
            )
            try:
                count = int(count_str)
                count = max(1, min(count, 20))
            except:
                count = 5

            self.display.console.print()

            # Generate passwords
            passwords = []
            for _ in range(count):
                password = self._generate_password(length, use_special)
                passwords.append(password)

            # Display passwords
            self.display.show_section("🔑 Generated Passwords")
            for i, pwd in enumerate(passwords, 1):
                self.display.console.print(f"  {i}. [green]{pwd}[/green]")

            self.display.console.print()
            self.display.show_info(
                "💡 Tip: Store passwords in a secure password manager"
            )

            return True

        except Exception as e:
            self.log_error("Password generation failed", e)
            self.display.show_error(f"Failed to generate passwords: {str(e)}")
            return False

    def _generate_password(self, length: int, use_special: bool) -> str:
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits
        if use_special:
            characters += string.punctuation

        # Ensure at least one of each type
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
        ]

        if use_special:
            password.append(secrets.choice(string.punctuation))

        # Fill the rest
        while len(password) < length:
            password.append(secrets.choice(characters))

        # Shuffle
        secrets.SystemRandom().shuffle(password)

        return "".join(password)


class HashGeneratorModule(BaseModule):
    """Generate and verify file/text hashes"""

    def __init__(self, display: Display):
        super().__init__(
            name="Hash Generator",
            description="Generate MD5, SHA1, SHA256 hashes",
            category="security",
        )
        self.display = display
        self.icon = "🔒"

    def execute(self) -> bool:
        try:
            self.display.console.print("1. Hash text")
            self.display.console.print("2. Hash file")
            self.display.console.print()

            choice = self.display.prompt("Choose option", default="1")

            if choice == "1":
                return self._hash_text()
            elif choice == "2":
                return self._hash_file()
            else:
                self.display.show_warning("Invalid choice")
                return False

        except Exception as e:
            self.log_error("Hash generation failed", e)
            self.display.show_error(f"Failed to generate hash: {str(e)}")
            return False

    def _hash_text(self) -> bool:
        """Hash text input"""
        text = self.display.prompt("Enter text to hash")

        if not text:
            self.display.show_warning("No text provided")
            return False

        self.display.console.print()

        hashes = {
            "MD5": hashlib.md5(text.encode()).hexdigest(),
            "SHA1": hashlib.sha1(text.encode()).hexdigest(),
            "SHA256": hashlib.sha256(text.encode()).hexdigest(),
            "SHA512": hashlib.sha512(text.encode()).hexdigest(),
        }

        self.display.show_key_value(hashes, "🔒 Text Hashes")
        return True

    def _hash_file(self) -> bool:
        """Hash file content"""
        filepath = self.display.prompt("Enter file path")

        if not filepath or not os.path.exists(filepath):
            self.display.show_error("File not found")
            return False

        self.display.console.print()
        self.display.show_info("Calculating hashes...")

        try:
            with open(filepath, "rb") as f:
                data = f.read()

            hashes = {
                "File": filepath,
                "Size": f"{len(data)} bytes",
                "MD5": hashlib.md5(data).hexdigest(),
                "SHA1": hashlib.sha1(data).hexdigest(),
                "SHA256": hashlib.sha256(data).hexdigest(),
                "SHA512": hashlib.sha512(data).hexdigest(),
            }

            self.display.show_key_value(hashes, "🔒 File Hashes")
            return True

        except Exception as e:
            self.display.show_error(f"Failed to read file: {str(e)}")
            return False


class MalwareScanModule(BaseModule):
    """Scan for malware and viruses"""

    def __init__(self, display: Display):
        super().__init__(
            name="Malware Scanner",
            description="Scan system for malware and viruses",
            category="security",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.executor = CommandExecutor(self.system_info)
        self.icon = "🦠"

    def execute(self) -> bool:
        try:
            # Check for available antivirus tools
            av_tools = {
                "clamav": "clamscan",
                "chkrootkit": "chkrootkit",
                "rkhunter": "rkhunter",
            }

            available_tools = []
            for name, cmd in av_tools.items():
                if self.system_info.is_command_available(cmd):
                    available_tools.append((name, cmd))

            if not available_tools:
                self.display.show_warning("No antivirus tools found")
                self.display.console.print()
                self.display.show_info("Available tools to install:")
                self.display.console.print("  • ClamAV: apt install clamav")
                self.display.console.print("  • chkrootkit: apt install chkrootkit")
                self.display.console.print("  • rkhunter: apt install rkhunter")
                return False

            self.display.show_info(f"Found {len(available_tools)} antivirus tool(s)")
            self.display.console.print()

            for name, cmd in available_tools:
                self.display.console.print(f"  • {name}")

            self.display.console.print()

            if not self.display.confirm("Start malware scan?", default=False):
                self.display.show_warning("Scan cancelled")
                return False

            # Run scans
            for name, cmd in available_tools:
                self.display.console.print()
                self.display.show_info(f"Running {name}...")
                self.display.console.print()

                if name == "clamav":
                    scan_cmd = f"{cmd} --infected --recursive --suppress-ok-results ~/"
                elif name == "chkrootkit":
                    scan_cmd = f"sudo {cmd}"
                elif name == "rkhunter":
                    scan_cmd = f"sudo {cmd} --check --skip-keypress"
                else:
                    scan_cmd = cmd

                try:
                    self.executor.run(scan_cmd, timeout=600)
                except:
                    self.display.show_warning(f"{name} scan had issues")

            self.display.console.print()
            self.display.show_success("Scan completed")
            return True

        except Exception as e:
            self.log_error("Malware scan failed", e)
            self.display.show_error(f"Scan failed: {str(e)}")
            return False


class FileEncryptionModule(BaseModule):
    """Simple file encryption/decryption"""

    def __init__(self, display: Display):
        super().__init__(
            name="File Encryption",
            description="Encrypt/decrypt files (simple XOR)",
            category="security",
        )
        self.display = display
        self.icon = "🔐"

    def execute(self) -> bool:
        try:
            self.display.console.print("1. Encrypt file")
            self.display.console.print("2. Decrypt file")
            self.display.console.print()

            choice = self.display.prompt("Choose option", default="1")

            if choice not in ["1", "2"]:
                self.display.show_warning("Invalid choice")
                return False

            filepath = self.display.prompt("Enter file path")
            if not os.path.exists(filepath):
                self.display.show_error("File not found")
                return False

            password = self.display.prompt("Enter password", password=True)
            if not password:
                self.display.show_warning("No password provided")
                return False

            output = self.display.prompt(
                "Output file path", default=filepath + ".encrypted"
            )

            self.display.console.print()

            if choice == "1":
                self._encrypt_file(filepath, output, password)
                self.display.show_success(f"File encrypted: {output}")
            else:
                self._decrypt_file(filepath, output, password)
                self.display.show_success(f"File decrypted: {output}")

            return True

        except Exception as e:
            self.log_error("Encryption operation failed", e)
            self.display.show_error(f"Operation failed: {str(e)}")
            return False

    def _encrypt_file(self, input_path: str, output_path: str, password: str):
        """Simple XOR encryption (NOT PRODUCTION GRADE!)"""
        key = hashlib.sha256(password.encode()).digest()

        with open(input_path, "rb") as f_in:
            data = f_in.read()

        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key[i % len(key)])

        with open(output_path, "wb") as f_out:
            f_out.write(encrypted)

    def _decrypt_file(self, input_path: str, output_path: str, password: str):
        """Simple XOR decryption"""
        # XOR encryption is symmetric
        self._encrypt_file(input_path, output_path, password)


def get_security_modules(display: Display) -> List[BaseModule]:
    """Get all security modules"""
    return [
        PasswordStrengthModule(display),
        PasswordGeneratorModule(display),
        HashGeneratorModule(display),
        MalwareScanModule(display),
        FileEncryptionModule(display),
    ]
