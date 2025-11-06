#!/usr/bin/env python3
"""
PyTools v2.0.0 - Network Module
Network diagnostics, monitoring and information tools
"""

import os
import sys
import socket
import subprocess
import re
import requests
from typing import Optional, Dict, List, Any

from core.base import (
    BaseModule,
    SystemInfo,
    CommandExecutor,
    validate_url,
    validate_ip,
)
from core.utils import get_logger, get_config
from ui.display import Display


class NetworkInfoModule(BaseModule):
    """Display network interface information"""

    def __init__(self, display: Display):
        super().__init__(
            name="Network Information",
            description="Display network interfaces and configuration",
            category="network",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.icon = "📡"

    def execute(self) -> bool:
        try:
            # Use ip command if available
            if self.system_info.is_command_available("ip"):
                self.display.show_info("Network Interfaces (ip addr):\n")
                os.system("ip addr show")
            elif self.system_info.is_command_available("ifconfig"):
                self.display.show_info("Network Interfaces (ifconfig):\n")
                os.system("ifconfig")
            else:
                # Fallback to basic info
                self._show_basic_network_info()

            return True
        except Exception as e:
            self.log_error("Failed to get network information", e)
            self.display.show_error(f"Failed to retrieve network info: {str(e)}")
            return False

    def _show_basic_network_info(self):
        """Show basic network information using Python"""
        import psutil

        info = {}

        # Get hostname
        info["Hostname"] = socket.gethostname()

        # Try to get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info["Local IP"] = s.getsockname()[0]
            s.close()
        except:
            info["Local IP"] = "Unable to detect"

        # Network interfaces
        interfaces = psutil.net_if_addrs()
        for iface, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    info[f"{iface} IPv4"] = addr.address

        self.display.show_key_value(info, "📡 Network Information")


class PingModule(BaseModule):
    """Ping a host or IP address"""

    def __init__(self, display: Display):
        super().__init__(
            name="Ping Host/IP",
            description="Test connectivity to a host or IP address",
            category="network",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.executor = CommandExecutor(self.system_info)
        self.icon = "📶"

    def execute(self) -> bool:
        try:
            host = self.display.prompt("Enter hostname or IP address to ping")

            if not host:
                self.display.show_warning("No host provided")
                return False

            # Check if online
            if not self.system_info.is_online():
                self.display.show_warning("No internet connection detected")

            self.display.console.print()
            self.display.show_section("🔍 Resolving Host Information")

            # Resolve hostname to IP
            ip_address = None
            hostname = None

            try:
                # Check if input is IP or hostname
                if validate_ip(host):
                    ip_address = host
                    # Try reverse DNS lookup
                    try:
                        hostname = socket.gethostbyaddr(host)[0]
                        self.display.console.print(
                            f"[cyan]IP Address:[/cyan] [green]{ip_address}[/green]"
                        )
                        self.display.console.print(
                            f"[cyan]Hostname:[/cyan] [yellow]{hostname}[/yellow]"
                        )
                    except:
                        self.display.console.print(
                            f"[cyan]IP Address:[/cyan] [green]{ip_address}[/green]"
                        )
                        self.display.console.print(
                            f"[cyan]Hostname:[/cyan] [dim]Not available[/dim]"
                        )
                else:
                    hostname = host
                    # Forward DNS lookup
                    ip_address = socket.gethostbyname(host)
                    self.display.console.print(
                        f"[cyan]Hostname:[/cyan] [yellow]{hostname}[/yellow]"
                    )
                    self.display.console.print(
                        f"[cyan]IP Address:[/cyan] [green]{ip_address}[/green]"
                    )

                    # Get all IPs for this hostname
                    try:
                        all_ips = socket.gethostbyname_ex(host)[2]
                        if len(all_ips) > 1:
                            self.display.console.print(
                                f"[cyan]Additional IPs:[/cyan] [dim]{', '.join(all_ips[1:])}[/dim]"
                            )
                    except:
                        pass

            except socket.gaierror:
                self.display.show_error(f"Could not resolve hostname: {host}")
                return False
            except Exception as e:
                self.display.show_error(f"DNS lookup failed: {str(e)}")
                return False

            self.display.console.print()
            self.display.show_section("📡 Ping Statistics")

            # Determine ping command based on OS
            if self.system_info.os_type == "windows":
                cmd = f"ping -n 8 {ip_address}"
            else:
                cmd = f"ping -c 8 -W 2 {ip_address}"

            # Execute ping and capture output
            result = self.executor.run(cmd, timeout=30, capture_output=True)

            if result.returncode == 0:
                self.display.console.print()

                # Parse ping output for detailed stats
                output = result.stdout

                # Show raw ping output with colors
                self._display_colored_ping_output(output)

                # Parse and display statistics
                self.display.console.print()
                self._parse_and_display_stats(output, ip_address, hostname or host)

                self.display.console.print()
                self.display.show_success(f"✓ Successfully pinged {hostname or host}")
                return True
            else:
                self.display.console.print()
                self.display.console.print(f"[red]{result.stdout}[/red]")
                self.display.console.print()
                self.display.show_error(f"✗ Failed to ping {host}")
                return False

        except Exception as e:
            self.log_error("Ping failed", e)
            self.display.show_error(f"Ping failed: {str(e)}")
            return False

    def _display_colored_ping_output(self, output: str):
        """Display ping output with syntax highlighting"""
        lines = output.split("\n")

        for line in lines:
            if not line.strip():
                continue

            # Highlight different parts of ping output
            if "bytes from" in line.lower() or "reply from" in line.lower():
                # Successful ping response
                parts = line.split()
                colored_line = ""
                for part in parts:
                    if "time=" in part or "time<" in part:
                        colored_line += f"[bright_green]{part}[/bright_green] "
                    elif "ttl=" in part.lower():
                        colored_line += f"[cyan]{part}[/cyan] "
                    elif "bytes" in part:
                        colored_line += f"[yellow]{part}[/yellow] "
                    else:
                        colored_line += f"{part} "
                self.display.console.print(f"  [green]✓[/green] {colored_line.strip()}")
            elif "packet loss" in line.lower() or "transmitted" in line.lower():
                # Statistics line
                self.display.console.print(f"[cyan]{line}[/cyan]")
            elif "min/" in line.lower() or "rtt" in line.lower():
                # RTT statistics
                self.display.console.print(f"[magenta]{line}[/magenta]")
            elif "timeout" in line.lower() or "unreachable" in line.lower():
                self.display.console.print(f"  [red]✗[/red] [red]{line}[/red]")
            else:
                self.display.console.print(f"[dim]{line}[/dim]")

    def _parse_and_display_stats(self, output: str, ip: str, host: str):
        """Parse ping output and display detailed statistics"""
        import re

        stats = {
            "Target": f"{host}" if host != ip else ip,
            "IP Address": ip,
        }

        # Parse packets transmitted/received
        transmitted = re.search(r"(\d+) packets transmitted", output)
        received = re.search(r"(\d+) received", output)
        loss = re.search(r"(\d+)% packet loss", output)

        if transmitted:
            stats["Packets Sent"] = transmitted.group(1)
        if received:
            stats["Packets Received"] = received.group(1)
            success_rate = (
                (int(received.group(1)) / int(transmitted.group(1)) * 100)
                if transmitted
                else 0
            )
            if success_rate == 100:
                stats["Success Rate"] = f"[green]{success_rate:.0f}%[/green]"
            elif success_rate >= 75:
                stats["Success Rate"] = f"[yellow]{success_rate:.0f}%[/yellow]"
            else:
                stats["Success Rate"] = f"[red]{success_rate:.0f}%[/red]"
        if loss:
            packet_loss = int(loss.group(1))
            if packet_loss == 0:
                stats["Packet Loss"] = f"[green]{packet_loss}%[/green]"
            elif packet_loss < 25:
                stats["Packet Loss"] = f"[yellow]{packet_loss}%[/yellow]"
            else:
                stats["Packet Loss"] = f"[red]{packet_loss}%[/red]"

        # Parse RTT (Round Trip Time) - multiple patterns for different OS
        rtt_patterns = [
            r"min/avg/max/(?:mdev|stddev) = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms",
            r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms",
            r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms",
        ]

        for pattern in rtt_patterns:
            rtt = re.search(pattern, output)
            if rtt:
                if len(rtt.groups()) >= 3:
                    min_rtt = float(rtt.group(1))
                    avg_rtt = float(rtt.group(2))
                    max_rtt = float(rtt.group(3))

                    # Color code based on latency
                    def color_latency(ms):
                        if ms < 30:
                            return f"[bright_green]{ms:.1f}ms[/bright_green]"
                        elif ms < 100:
                            return f"[green]{ms:.1f}ms[/green]"
                        elif ms < 200:
                            return f"[yellow]{ms:.1f}ms[/yellow]"
                        elif ms < 500:
                            return f"[orange]{ms:.1f}ms[/orange]"
                        else:
                            return f"[red]{ms:.1f}ms[/red]"

                    stats["Min Latency"] = color_latency(min_rtt)
                    stats["Avg Latency"] = color_latency(avg_rtt)
                    stats["Max Latency"] = color_latency(max_rtt)

                    if len(rtt.groups()) >= 4:
                        stats["Std Deviation"] = f"{float(rtt.group(4)):.1f}ms"

                    # Connection quality assessment
                    if avg_rtt < 30:
                        quality = "[bright_green]Excellent[/bright_green] ⚡"
                    elif avg_rtt < 100:
                        quality = "[green]Good[/green] ✓"
                    elif avg_rtt < 200:
                        quality = "[yellow]Fair[/yellow] ~"
                    elif avg_rtt < 500:
                        quality = "[orange]Poor[/orange] ⚠"
                    else:
                        quality = "[red]Very Poor[/red] ✗"

                    stats["Connection Quality"] = quality
                break

        # Display statistics in a nice table
        from rich.table import Table

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Metric", style="cyan bold")
        table.add_column("Value", style="white")

        for key, value in stats.items():
            table.add_row(key, value)

        from rich.panel import Panel

        panel = Panel(
            table,
            title="[bold bright_cyan]📊 Detailed Statistics[/bold bright_cyan]",
            border_style="cyan",
        )

        self.display.console.print(panel)


class TracerouteModule(BaseModule):
    """Perform traceroute to destination"""

    def __init__(self, display: Display):
        super().__init__(
            name="Traceroute",
            description="Trace the route packets take to a destination",
            category="network",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.executor = CommandExecutor(self.system_info)
        self.icon = "🗺️"

    def execute(self) -> bool:
        try:
            host = self.display.prompt("Enter hostname or IP for traceroute")

            if not host:
                self.display.show_warning("No host provided")
                return False

            self.display.console.print()
            self.display.show_info(f"Performing traceroute to {host}...\n")

            # Determine command based on OS
            if self.system_info.os_type == "windows":
                cmd = f"tracert {host}"
            else:
                if self.system_info.is_command_available("traceroute"):
                    cmd = f"traceroute {host}"
                elif self.system_info.is_command_available("tracepath"):
                    cmd = f"tracepath {host}"
                else:
                    self.display.show_error("Traceroute command not available")
                    return False

            # Execute traceroute
            result = self.executor.run(cmd, timeout=120)

            self.display.console.print()
            if result.returncode == 0:
                self.display.show_success("Traceroute completed")
                return True
            else:
                self.display.show_warning("Traceroute completed with errors")
                return False

        except Exception as e:
            self.log_error("Traceroute failed", e)
            self.display.show_error(f"Traceroute failed: {str(e)}")
            return False


class PortScannerModule(BaseModule):
    """Scan ports on a host"""

    def __init__(self, display: Display):
        super().__init__(
            name="Port Scanner",
            description="Scan common ports on a host",
            category="network",
        )
        self.display = display
        self.icon = "🔍"

    def execute(self) -> bool:
        try:
            host = self.display.prompt("Enter hostname or IP to scan")

            if not host:
                self.display.show_warning("No host provided")
                return False

            # Resolve hostname to IP
            try:
                ip = socket.gethostbyname(host)
                self.display.show_info(f"Scanning {host} ({ip})...")
            except:
                self.display.show_error(f"Could not resolve {host}")
                return False

            # Common ports to scan
            common_ports = {
                20: "FTP Data",
                21: "FTP Control",
                22: "SSH",
                23: "Telnet",
                25: "SMTP",
                53: "DNS",
                80: "HTTP",
                110: "POP3",
                143: "IMAP",
                443: "HTTPS",
                445: "SMB",
                3306: "MySQL",
                3389: "RDP",
                5432: "PostgreSQL",
                8080: "HTTP Alt",
            }

            self.display.console.print()
            open_ports = []

            with self.display.show_progress_bar(
                len(common_ports), "Scanning ports..."
            ) as progress:
                task = progress.add_task("Scanning...", total=len(common_ports))

                for port, service in common_ports.items():
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip, port))
                    sock.close()

                    if result == 0:
                        open_ports.append([str(port), service, "OPEN"])

                    progress.update(task, advance=1)

            self.display.console.print()

            if open_ports:
                headers = ["Port", "Service", "Status"]
                self.display.show_table(
                    f"🔍 Open Ports on {host}",
                    headers,
                    open_ports,
                    colors=["cyan", "yellow", "green"],
                )
                return True
            else:
                self.display.show_info("No open ports found (common ports only)")
                return True

        except Exception as e:
            self.log_error("Port scan failed", e)
            self.display.show_error(f"Port scan failed: {str(e)}")
            return False


class SpeedTestModule(BaseModule):
    """Test internet connection speed"""

    def __init__(self, display: Display):
        super().__init__(
            name="Internet Speed Test",
            description="Test download and upload speeds",
            category="network",
        )
        self.display = display
        self.icon = "⚡"

    def execute(self) -> bool:
        try:
            # Check if speedtest-cli is available
            import speedtest

            self.display.show_info("Starting speed test...")
            self.display.show_warning("This may take a minute...\n")

            st = speedtest.Speedtest()

            # Get best server
            self.display.show_info("Finding best server...")
            st.get_best_server()

            # Download test
            self.display.show_info("Testing download speed...")
            download_speed = st.download() / 1_000_000  # Convert to Mbps

            # Upload test
            self.display.show_info("Testing upload speed...")
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps

            # Get ping
            ping = st.results.ping

            # Display results
            self.display.console.print()
            results = {
                "Download Speed": f"{download_speed:.2f} Mbps",
                "Upload Speed": f"{upload_speed:.2f} Mbps",
                "Ping": f"{ping:.2f} ms",
                "Server": st.results.server["sponsor"],
                "Location": f"{st.results.server['name']}, {st.results.server['country']}",
            }

            self.display.show_key_value(results, "⚡ Speed Test Results")

            return True

        except ImportError:
            self.display.show_error("speedtest-cli module not installed")
            self.display.show_info("Install with: pip install speedtest-cli")
            return False
        except Exception as e:
            self.log_error("Speed test failed", e)
            self.display.show_error(f"Speed test failed: {str(e)}")
            return False


class DNSLookupModule(BaseModule):
    """Perform DNS lookup"""

    def __init__(self, display: Display):
        super().__init__(
            name="DNS Lookup",
            description="Resolve domain names to IP addresses",
            category="network",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.icon = "🔎"

    def execute(self) -> bool:
        try:
            domain = self.display.prompt("Enter domain name to lookup")

            if not domain:
                self.display.show_warning("No domain provided")
                return False

            self.display.console.print()

            info = {}

            # Get IPv4 addresses
            try:
                ipv4_list = socket.getaddrinfo(domain, None, socket.AF_INET)
                ipv4_addrs = list(set([addr[4][0] for addr in ipv4_list]))
                info["IPv4 Addresses"] = ", ".join(ipv4_addrs)
            except:
                info["IPv4 Addresses"] = "Not found"

            # Get IPv6 addresses
            try:
                ipv6_list = socket.getaddrinfo(domain, None, socket.AF_INET6)
                ipv6_addrs = list(set([addr[4][0] for addr in ipv6_list]))
                info["IPv6 Addresses"] = ", ".join(ipv6_addrs)
            except:
                info["IPv6 Addresses"] = "Not found"

            # Try using dig/nslookup if available
            if self.system_info.is_command_available("dig"):
                self.display.show_key_value(info, f"🔎 DNS Lookup: {domain}")
                self.display.console.print()
                self.display.show_info("Detailed DNS records (dig):\n")
                os.system(f"dig {domain}")
            elif self.system_info.is_command_available("nslookup"):
                self.display.show_key_value(info, f"🔎 DNS Lookup: {domain}")
                self.display.console.print()
                self.display.show_info("Detailed DNS records (nslookup):\n")
                os.system(f"nslookup {domain}")
            else:
                self.display.show_key_value(info, f"🔎 DNS Lookup: {domain}")

            return True

        except Exception as e:
            self.log_error("DNS lookup failed", e)
            self.display.show_error(f"DNS lookup failed: {str(e)}")
            return False


class WHOISLookupModule(BaseModule):
    """Perform WHOIS lookup"""

    def __init__(self, display: Display):
        super().__init__(
            name="WHOIS Lookup",
            description="Get WHOIS information for a domain",
            category="network",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.executor = CommandExecutor(self.system_info)
        self.icon = "📋"

    def execute(self) -> bool:
        try:
            domain = self.display.prompt("Enter domain name for WHOIS lookup")

            if not domain:
                self.display.show_warning("No domain provided")
                return False

            self.display.console.print()
            self.display.show_info(f"Performing WHOIS lookup for {domain}...\n")

            if self.system_info.is_command_available("whois"):
                os.system(f"whois {domain}")
                return True
            else:
                # Try using python-whois if available
                try:
                    import whois

                    w = whois.whois(domain)

                    info = {}
                    if hasattr(w, "registrar") and w.registrar:
                        info["Registrar"] = w.registrar
                    if hasattr(w, "creation_date") and w.creation_date:
                        info["Created"] = str(w.creation_date)
                    if hasattr(w, "expiration_date") and w.expiration_date:
                        info["Expires"] = str(w.expiration_date)
                    if hasattr(w, "name_servers") and w.name_servers:
                        info["Name Servers"] = ", ".join(w.name_servers)

                    if info:
                        self.display.show_key_value(info, f"📋 WHOIS: {domain}")
                        return True
                    else:
                        self.display.show_warning("No WHOIS information found")
                        return False

                except ImportError:
                    self.display.show_error("whois command not available")
                    self.display.show_info("Install with: pip install python-whois")
                    return False

        except Exception as e:
            self.log_error("WHOIS lookup failed", e)
            self.display.show_error(f"WHOIS lookup failed: {str(e)}")
            return False


def get_network_modules(display: Display) -> List[BaseModule]:
    """Get all network modules"""
    return [
        NetworkInfoModule(display),
        PingModule(display),
        TracerouteModule(display),
        PortScannerModule(display),
        SpeedTestModule(display),
        DNSLookupModule(display),
        WHOISLookupModule(display),
    ]
