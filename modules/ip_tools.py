#!/usr/bin/env python3
"""
PyTools v2.0.0 - IP Tools Module
IP address utilities, geolocation, and network information
"""

import socket
import requests
from typing import Optional, Dict, List, Any

from core.base import BaseModule, SystemInfo, validate_ip
from core.utils import get_logger, get_config
from ui.display import Display


class GeolocateIPModule(BaseModule):
    """Geolocate an IP address"""

    def __init__(self, display: Display):
        super().__init__(
            name="Geolocate IP",
            description="Get geographical location of an IP address",
            category="ip",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.icon = "🌍"

    def execute(self) -> bool:
        try:
            ip = self.display.prompt(
                "Enter IP address to geolocate (or press Enter for your IP)"
            )

            if not ip:
                # Get user's public IP
                self.display.show_info("Detecting your public IP...")
                ip = self._get_public_ip()
                if not ip:
                    self.display.show_error("Failed to detect your IP")
                    return False
                self.display.show_info(f"Your public IP: {ip}")

            if not validate_ip(ip):
                self.display.show_error("Invalid IP address format")
                return False

            self.display.console.print()
            self.display.show_info(f"Geolocating {ip}...")

            # Get geolocation data
            geo_data = self._get_geolocation(ip)

            if geo_data:
                self.display.console.print()
                self.display.show_key_value(geo_data, f"🌍 Geolocation: {ip}")
                return True
            else:
                self.display.show_error("Failed to retrieve geolocation data")
                return False

        except Exception as e:
            self.log_error("Geolocation failed", e)
            self.display.show_error(f"Geolocation failed: {str(e)}")
            return False

    def _get_public_ip(self) -> Optional[str]:
        """Get user's public IP address"""
        services = [
            "https://api.ipify.org",
            "https://icanhazip.com",
            "https://ident.me",
        ]

        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue

        return None

    def _get_geolocation(self, ip: str) -> Optional[Dict[str, str]]:
        """Get geolocation data for IP"""
        services = [
            f"https://ipapi.co/{ip}/json/",
            f"https://ipinfo.io/{ip}/json",
        ]

        for service in services:
            try:
                response = requests.get(service, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    return self._format_geo_data(data)
            except:
                continue

        return None

    def _format_geo_data(self, data: dict) -> Dict[str, str]:
        """Format geolocation data"""
        formatted = {}

        # Common fields across different APIs
        field_mappings = {
            "ip": ["ip"],
            "city": ["city"],
            "region": ["region", "region_name"],
            "country": ["country", "country_name"],
            "country_code": ["country_code"],
            "postal": ["postal", "zip"],
            "latitude": ["latitude", "lat"],
            "longitude": ["longitude", "lon", "lng"],
            "timezone": ["timezone"],
            "isp": ["org", "isp"],
        }

        for key, possible_fields in field_mappings.items():
            for field in possible_fields:
                if field in data and data[field]:
                    formatted[key.replace("_", " ").title()] = str(data[field])
                    break

        return formatted


class MyPublicIPModule(BaseModule):
    """Get your public IP address"""

    def __init__(self, display: Display):
        super().__init__(
            name="My Public IP",
            description="Display your public IP address and information",
            category="ip",
        )
        self.display = display
        self.icon = "🌐"

    def execute(self) -> bool:
        try:
            self.display.show_info("Detecting your public IP address...")
            self.display.console.print()

            # Get public IP
            ip = self._get_public_ip()

            if not ip:
                self.display.show_error("Failed to detect public IP")
                return False

            # Get additional info
            info = self._get_ip_info(ip)

            if info:
                self.display.show_key_value(info, "🌐 Your Public IP Information")
            else:
                self.display.show_info(f"Your Public IP: {ip}")

            return True

        except Exception as e:
            self.log_error("Failed to get public IP", e)
            self.display.show_error(f"Failed to get public IP: {str(e)}")
            return False

    def _get_public_ip(self) -> Optional[str]:
        """Get public IP address"""
        services = [
            "https://api.ipify.org",
            "https://icanhazip.com",
            "https://ident.me",
            "https://ifconfig.me/ip",
        ]

        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    return response.text.strip()
            except:
                continue

        return None

    def _get_ip_info(self, ip: str) -> Optional[Dict[str, str]]:
        """Get detailed IP information"""
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()

                info = {
                    "IP Address": ip,
                    "Version": f"IPv{data.get('version', 'Unknown')}",
                    "City": data.get("city", "Unknown"),
                    "Region": data.get("region", "Unknown"),
                    "Country": data.get("country_name", "Unknown"),
                    "Country Code": data.get("country_code", "Unknown"),
                    "Timezone": data.get("timezone", "Unknown"),
                    "ISP": data.get("org", "Unknown"),
                    "ASN": data.get("asn", "Unknown"),
                    "Latitude": str(data.get("latitude", "Unknown")),
                    "Longitude": str(data.get("longitude", "Unknown")),
                }

                return info

        except:
            pass

        return None


class IPCalculatorModule(BaseModule):
    """IP address calculator and subnet information"""

    def __init__(self, display: Display):
        super().__init__(
            name="IP Calculator",
            description="Calculate subnet information for IP addresses",
            category="ip",
        )
        self.display = display
        self.icon = "🔢"

    def execute(self) -> bool:
        try:
            ip_input = self.display.prompt(
                "Enter IP address with CIDR (e.g., 192.168.1.0/24)"
            )

            if not ip_input or "/" not in ip_input:
                self.display.show_error(
                    "Invalid format. Use: IP/CIDR (e.g., 192.168.1.0/24)"
                )
                return False

            # Parse IP and CIDR
            try:
                ip_str, cidr_str = ip_input.split("/")
                cidr = int(cidr_str)

                if not validate_ip(ip_str):
                    self.display.show_error("Invalid IP address")
                    return False

                if not (0 <= cidr <= 32):
                    self.display.show_error("CIDR must be between 0 and 32")
                    return False

            except ValueError:
                self.display.show_error("Invalid format")
                return False

            self.display.console.print()

            # Calculate subnet info
            info = self._calculate_subnet(ip_str, cidr)

            if info:
                self.display.show_key_value(info, f"🔢 Subnet Information: {ip_input}")
                return True
            else:
                self.display.show_error("Failed to calculate subnet")
                return False

        except Exception as e:
            self.log_error("IP calculation failed", e)
            self.display.show_error(f"Calculation failed: {str(e)}")
            return False

    def _calculate_subnet(self, ip: str, cidr: int) -> Dict[str, str]:
        """Calculate subnet information"""
        # Convert IP to integer
        ip_int = self._ip_to_int(ip)

        # Calculate subnet mask
        mask_int = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
        mask = self._int_to_ip(mask_int)

        # Calculate network address
        network_int = ip_int & mask_int
        network = self._int_to_ip(network_int)

        # Calculate broadcast address
        wildcard_int = 0xFFFFFFFF ^ mask_int
        broadcast_int = network_int | wildcard_int
        broadcast = self._int_to_ip(broadcast_int)

        # Calculate first and last usable IPs
        first_usable = self._int_to_ip(network_int + 1) if cidr < 31 else network
        last_usable = self._int_to_ip(broadcast_int - 1) if cidr < 31 else broadcast

        # Calculate total hosts
        total_hosts = 2 ** (32 - cidr)
        usable_hosts = max(0, total_hosts - 2) if cidr < 31 else total_hosts

        # Calculate wildcard mask
        wildcard = self._int_to_ip(wildcard_int)

        info = {
            "IP Address": ip,
            "Network Address": network,
            "Subnet Mask": mask,
            "Wildcard Mask": wildcard,
            "Broadcast Address": broadcast,
            "First Usable IP": first_usable,
            "Last Usable IP": last_usable,
            "CIDR Notation": f"/{cidr}",
            "Total Addresses": str(total_hosts),
            "Usable Addresses": str(usable_hosts),
            "IP Class": self._get_ip_class(ip),
        }

        return info

    def _ip_to_int(self, ip: str) -> int:
        """Convert IP address string to integer"""
        parts = [int(part) for part in ip.split(".")]
        return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + parts[3]

    def _int_to_ip(self, ip_int: int) -> str:
        """Convert integer to IP address string"""
        return f"{(ip_int >> 24) & 0xFF}.{(ip_int >> 16) & 0xFF}.{(ip_int >> 8) & 0xFF}.{ip_int & 0xFF}"

    def _get_ip_class(self, ip: str) -> str:
        """Determine IP address class"""
        first_octet = int(ip.split(".")[0])

        if 1 <= first_octet <= 126:
            return "A (Public)"
        elif first_octet == 127:
            return "A (Loopback)"
        elif 128 <= first_octet <= 191:
            return "B"
        elif 192 <= first_octet <= 223:
            return "C"
        elif 224 <= first_octet <= 239:
            return "D (Multicast)"
        elif 240 <= first_octet <= 255:
            return "E (Reserved)"
        else:
            return "Unknown"


def get_ip_modules(display: Display) -> List[BaseModule]:
    """Get all IP tool modules"""
    return [
        GeolocateIPModule(display),
        MyPublicIPModule(display),
        IPCalculatorModule(display),
    ]
