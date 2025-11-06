#!/usr/bin/env python3
"""
PyTools v2.0.0 - System Module
System monitoring, management and maintenance tools
"""

import os
import sys
import platform
import subprocess
import psutil
from datetime import datetime
from typing import Optional, Dict, List, Any

from core.base import (
    BaseModule,
    SystemInfo,
    CommandExecutor,
    format_bytes,
    format_duration,
)
from core.utils import get_logger, get_config
from ui.display import Display


class SystemInformationModule(BaseModule):
    """Display comprehensive system information"""

    def __init__(self, display: Display):
        super().__init__(
            name="System Information",
            description="Display detailed system information",
            category="system",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.icon = "💻"

    def execute(self) -> bool:
        try:
            info = self._gather_system_info()

            # Show with neofetch if available
            if self.system_info.is_command_available("neofetch"):
                self.display.show_info("Fetching system information with neofetch...\n")
                os.system("neofetch")
                self.display.console.print()

            # Show detailed info
            self.display.show_key_value(info, "📊 Detailed System Information")

            return True
        except Exception as e:
            self.log_error("Failed to get system information", e)
            self.display.show_error(f"Failed to retrieve system information: {str(e)}")
            return False

    def _gather_system_info(self) -> Dict[str, str]:
        """Gather comprehensive system information"""
        info = {}

        try:
            # Basic info
            info["OS"] = f"{platform.system()} {platform.release()}"
            info["OS Version"] = platform.version()
            info["Architecture"] = platform.machine()
            info["Processor"] = platform.processor() or "Unknown"
            info["Python Version"] = platform.python_version()
            info["Hostname"] = platform.node()

            # CPU info
            info["CPU Cores"] = str(psutil.cpu_count(logical=False))
            info["CPU Threads"] = str(psutil.cpu_count(logical=True))
            info["CPU Usage"] = f"{psutil.cpu_percent(interval=1)}%"

            # Memory info
            mem = psutil.virtual_memory()
            info["Total RAM"] = format_bytes(mem.total)
            info["Available RAM"] = format_bytes(mem.available)
            info["Used RAM"] = f"{format_bytes(mem.used)} ({mem.percent}%)"

            # Disk info
            disk = psutil.disk_usage("/")
            info["Total Disk"] = format_bytes(disk.total)
            info["Used Disk"] = f"{format_bytes(disk.used)} ({disk.percent}%)"
            info["Free Disk"] = format_bytes(disk.free)

            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            info["Boot Time"] = boot_time.strftime("%Y-%m-%d %H:%M:%S")

            # Uptime
            uptime_seconds = int((datetime.now() - boot_time).total_seconds())
            info["Uptime"] = format_duration(uptime_seconds)

        except Exception as e:
            self.log_warning(f"Error gathering some system info: {e}")

        return info


class SystemUptimeModule(BaseModule):
    """Display system uptime"""

    def __init__(self, display: Display):
        super().__init__(
            name="System Uptime",
            description="Show how long the system has been running",
            category="system",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.icon = "⏱️"

    def execute(self) -> bool:
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            current_time = datetime.now()
            uptime = current_time - boot_time

            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            info = {
                "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Current Time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "Total Uptime": f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds",
                "Days": str(days),
                "Hours": str(hours),
                "Minutes": str(minutes),
            }

            self.display.show_key_value(info, "⏱️ System Uptime")

            # Try to use system uptime command if available
            if self.system_info.is_command_available("uptime"):
                self.display.console.print()
                self.display.show_info("System uptime command output:")
                os.system("uptime")

            return True
        except Exception as e:
            self.log_error("Failed to get system uptime", e)
            self.display.show_error(f"Failed to retrieve uptime: {str(e)}")
            return False


class DiskUsageModule(BaseModule):
    """Display disk usage information"""

    def __init__(self, display: Display):
        super().__init__(
            name="Disk Usage",
            description="Display disk space usage for all partitions",
            category="system",
        )
        self.display = display
        self.icon = "💾"

    def execute(self) -> bool:
        try:
            partitions = psutil.disk_partitions()

            # Prepare table data
            headers = [
                "Device",
                "Mount Point",
                "FS Type",
                "Total",
                "Used",
                "Free",
                "Usage %",
            ]
            rows = []

            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)

                    # Create visual bar
                    bar_length = 20
                    used_blocks = int((usage.percent / 100) * bar_length)
                    bar = "█" * used_blocks + "░" * (bar_length - used_blocks)

                    rows.append(
                        [
                            partition.device,
                            partition.mountpoint,
                            partition.fstype,
                            format_bytes(usage.total),
                            format_bytes(usage.used),
                            format_bytes(usage.free),
                            f"{usage.percent}% {bar}",
                        ]
                    )
                except PermissionError:
                    continue

            if rows:
                self.display.show_table("💾 Disk Usage", headers, rows)
            else:
                self.display.show_warning("No accessible disk partitions found")

            return True
        except Exception as e:
            self.log_error("Failed to get disk usage", e)
            self.display.show_error(f"Failed to retrieve disk usage: {str(e)}")
            return False


class MemoryUsageModule(BaseModule):
    """Display memory usage information"""

    def __init__(self, display: Display):
        super().__init__(
            name="Memory Usage",
            description="Display RAM and swap memory usage",
            category="system",
        )
        self.display = display
        self.icon = "🧠"

    def execute(self) -> bool:
        try:
            # Virtual memory
            mem = psutil.virtual_memory()

            # Swap memory
            swap = psutil.swap_memory()

            # Create visual bars
            def create_bar(percent):
                bar_length = 30
                used_blocks = int((percent / 100) * bar_length)
                return "█" * used_blocks + "░" * (bar_length - used_blocks)

            # RAM info
            ram_info = {
                "Total": format_bytes(mem.total),
                "Available": format_bytes(mem.available),
                "Used": format_bytes(mem.used),
                "Percentage": f"{mem.percent}%",
                "Visual": create_bar(mem.percent),
            }

            self.display.show_key_value(ram_info, "🧠 RAM Usage")
            self.display.console.print()

            # Swap info
            if swap.total > 0:
                swap_info = {
                    "Total": format_bytes(swap.total),
                    "Used": format_bytes(swap.used),
                    "Free": format_bytes(swap.free),
                    "Percentage": f"{swap.percent}%",
                    "Visual": create_bar(swap.percent),
                }
                self.display.show_key_value(swap_info, "💿 SWAP Usage")
            else:
                self.display.show_info("No swap memory configured")

            return True
        except Exception as e:
            self.log_error("Failed to get memory usage", e)
            self.display.show_error(f"Failed to retrieve memory usage: {str(e)}")
            return False


class ProcessListModule(BaseModule):
    """List running processes"""

    def __init__(self, display: Display):
        super().__init__(
            name="List Running Processes",
            description="Display list of running processes with resource usage",
            category="system",
        )
        self.display = display
        self.icon = "⚙️"

    def execute(self) -> bool:
        try:
            self.display.show_info("Gathering process information...")

            # Get all processes
            processes = []
            for proc in psutil.process_iter(
                ["pid", "name", "username", "memory_percent", "cpu_percent"]
            ):
                try:
                    pinfo = proc.info
                    processes.append(
                        [
                            str(pinfo["pid"]),
                            pinfo["name"][:30],
                            pinfo["username"][:15] if pinfo["username"] else "N/A",
                            f"{pinfo['memory_percent']:.1f}%",
                            f"{pinfo['cpu_percent']:.1f}%",
                        ]
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Sort by memory usage
            processes.sort(key=lambda x: float(x[3].rstrip("%")), reverse=True)

            # Show top 20 processes
            headers = ["PID", "Name", "User", "Memory %", "CPU %"]
            self.display.show_table(
                f"⚙️ Top {min(20, len(processes))} Processes (by Memory Usage)",
                headers,
                processes[:20],
            )

            self.display.console.print()
            self.display.show_info(f"Total processes running: {len(processes)}")

            return True
        except Exception as e:
            self.log_error("Failed to list processes", e)
            self.display.show_error(f"Failed to retrieve process list: {str(e)}")
            return False


class SystemUpdateModule(BaseModule):
    """Update system packages"""

    def __init__(self, display: Display):
        super().__init__(
            name="Update System",
            description="Update system packages and dependencies",
            category="system",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.executor = CommandExecutor(self.system_info)
        self.icon = "🔄"

    def execute(self) -> bool:
        try:
            pkg_manager = self.system_info.package_manager

            if pkg_manager == "unknown":
                self.display.show_error("Could not detect package manager")
                return False

            self.display.show_info(f"Using package manager: {pkg_manager}")
            self.display.console.print()

            # Confirm action
            if not self.display.confirm(
                "Do you want to update the system?", default=False
            ):
                self.display.show_warning("Update cancelled")
                return False

            self.display.console.print()

            # Update based on package manager
            if pkg_manager in ["apt", "apt-get"]:
                self._update_apt()
            elif pkg_manager == "pkg":
                self._update_termux()
            elif pkg_manager == "dnf":
                self._update_dnf()
            elif pkg_manager == "yum":
                self._update_yum()
            elif pkg_manager == "pacman":
                self._update_pacman()
            elif pkg_manager == "brew":
                self._update_brew()
            else:
                self.display.show_error(f"Update not implemented for {pkg_manager}")
                return False

            self.display.show_success("System update completed!")
            return True

        except Exception as e:
            self.log_error("System update failed", e)
            self.display.show_error(f"Update failed: {str(e)}")
            return False

    def _update_apt(self):
        """Update using apt"""
        commands = [
            ("sudo apt update -y", "Updating package lists..."),
            ("sudo apt upgrade -y", "Upgrading packages..."),
            ("sudo apt autoremove -y", "Removing unused packages..."),
            ("sudo apt autoclean", "Cleaning package cache..."),
        ]
        self._run_commands(commands)

    def _update_termux(self):
        """Update using Termux pkg"""
        commands = [
            ("pkg update -y", "Updating package lists..."),
            ("pkg upgrade -y", "Upgrading packages..."),
            ("pkg autoclean", "Cleaning package cache..."),
        ]
        self._run_commands(commands)

    def _update_dnf(self):
        """Update using dnf"""
        commands = [
            ("sudo dnf upgrade -y", "Upgrading packages..."),
            ("sudo dnf autoremove -y", "Removing unused packages..."),
        ]
        self._run_commands(commands)

    def _update_yum(self):
        """Update using yum"""
        commands = [
            ("sudo yum update -y", "Updating packages..."),
        ]
        self._run_commands(commands)

    def _update_pacman(self):
        """Update using pacman"""
        commands = [
            ("sudo pacman -Syu --noconfirm", "Updating packages..."),
        ]
        self._run_commands(commands)

    def _update_brew(self):
        """Update using Homebrew"""
        commands = [
            ("brew update", "Updating Homebrew..."),
            ("brew upgrade", "Upgrading packages..."),
            ("brew cleanup", "Cleaning up..."),
        ]
        self._run_commands(commands)

    def _run_commands(self, commands: List[tuple]):
        """Run list of commands"""
        for cmd, desc in commands:
            self.display.show_info(desc)
            try:
                result = self.executor.run(cmd, timeout=300)
                if result.returncode == 0:
                    self.display.show_success(f"✓ {desc.rstrip('...')}")
                else:
                    self.display.show_warning(
                        f"⚠ {desc.rstrip('...')} (exit code: {result.returncode})"
                    )
            except Exception as e:
                self.display.show_error(f"✗ {desc.rstrip('...')}: {str(e)}")
            self.display.console.print()


class SystemCleanModule(BaseModule):
    """Clean system temporary files and caches"""

    def __init__(self, display: Display):
        super().__init__(
            name="Clean System",
            description="Clean temporary files, caches, and logs",
            category="system",
        )
        self.display = display
        self.system_info = SystemInfo()
        self.executor = CommandExecutor(self.system_info)
        self.icon = "🧹"

    def execute(self) -> bool:
        try:
            self.display.show_warning("This will clean temporary files and caches")

            if not self.display.confirm("Continue with system cleanup?", default=False):
                self.display.show_warning("Cleanup cancelled")
                return False

            self.display.console.print()
            freed_space = 0

            # Clean based on OS
            if self.system_info.os_type == "linux":
                freed_space = self._clean_linux()
            elif self.system_info.os_type == "darwin":
                freed_space = self._clean_macos()
            elif self.system_info.os_type == "windows":
                self.display.show_info("Windows cleanup not fully implemented")
                return False

            if freed_space > 0:
                self.display.show_success(
                    f"Cleanup completed! Freed approximately {format_bytes(freed_space)}"
                )
            else:
                self.display.show_info("Cleanup completed!")

            return True

        except Exception as e:
            self.log_error("System cleanup failed", e)
            self.display.show_error(f"Cleanup failed: {str(e)}")
            return False

    def _clean_linux(self) -> int:
        """Clean Linux system"""
        freed = 0

        # Clean package cache
        if self.system_info.package_manager in ["apt", "apt-get"]:
            self.display.show_info("Cleaning APT cache...")
            self.executor.run_silent("sudo apt clean")
            self.executor.run_silent("sudo apt autoclean")

        # Clean thumbnail cache
        thumb_cache = os.path.expanduser("~/.cache/thumbnails")
        if os.path.exists(thumb_cache):
            self.display.show_info("Cleaning thumbnail cache...")
            try:
                import shutil

                size = self._get_dir_size(thumb_cache)
                shutil.rmtree(thumb_cache, ignore_errors=True)
                freed += size
            except:
                pass

        # Clean temp files
        temp_dirs = ["/tmp", "/var/tmp"]
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir) and os.access(temp_dir, os.W_OK):
                self.display.show_info(f"Cleaning {temp_dir}...")
                try:
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        if os.path.isfile(item_path):
                            try:
                                size = os.path.getsize(item_path)
                                os.remove(item_path)
                                freed += size
                            except:
                                pass
                except:
                    pass

        return freed

    def _clean_macos(self) -> int:
        """Clean macOS system"""
        freed = 0

        # Clean user cache
        cache_dir = os.path.expanduser("~/Library/Caches")
        if os.path.exists(cache_dir):
            self.display.show_info("Cleaning user caches...")
            # Only clean safe caches
            # Implementation would go here

        return freed

    def _get_dir_size(self, path: str) -> int:
        """Get directory size in bytes"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += self._get_dir_size(entry.path)
        except:
            pass
        return total


def get_system_modules(display: Display) -> List[BaseModule]:
    """Get all system modules"""
    return [
        SystemInformationModule(display),
        SystemUptimeModule(display),
        DiskUsageModule(display),
        MemoryUsageModule(display),
        ProcessListModule(display),
        SystemUpdateModule(display),
        SystemCleanModule(display),
    ]
