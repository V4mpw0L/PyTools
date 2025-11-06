#!/usr/bin/env python3
"""
PyTools v2.0.0 - Core Base Module
Base classes and core functionality for all modules
"""

import os
import sys
import logging
import subprocess
import platform
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime


class BaseModule(ABC):
    """Base class for all PyTools modules"""

    def __init__(self, name: str, description: str, category: str):
        self.name = name
        self.description = description
        self.category = category
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup module-specific logger"""
        logger = logging.getLogger(f"pytools.{self.name}")
        return logger

    @abstractmethod
    def execute(self) -> bool:
        """Execute the module's main functionality"""
        pass

    def log_info(self, message: str):
        """Log info message"""
        self.logger.info(f"[{self.name}] {message}")

    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log error message"""
        if exception:
            self.logger.error(
                f"[{self.name}] {message}: {str(exception)}", exc_info=True
            )
        else:
            self.logger.error(f"[{self.name}] {message}")

    def log_warning(self, message: str):
        """Log warning message"""
        self.logger.warning(f"[{self.name}] {message}")


class SystemInfo:
    """System information detector"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemInfo, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._detect_system()

    def _detect_system(self):
        """Detect system information"""
        self.os_type = platform.system().lower()
        self.os_version = platform.version()
        self.os_release = platform.release()
        self.machine = platform.machine()
        self.processor = platform.processor()
        self.python_version = platform.python_version()

        # Detect Termux environment
        self.is_termux = self._is_termux()

        # Detect if running as root
        self.is_root = os.geteuid() == 0 if hasattr(os, "geteuid") else False

        # Detect shell
        self.shell = os.environ.get("SHELL", "unknown")

        # Set package manager
        self.package_manager = self._detect_package_manager()

    def _is_termux(self) -> bool:
        """Check if running in Termux"""
        try:
            return os.environ.get("PREFIX", "").startswith("/data/data/com.termux")
        except:
            return False

    def _detect_package_manager(self) -> str:
        """Detect the system's package manager"""
        if self.is_termux:
            return "pkg"
        elif self.os_type == "linux":
            # Check for various package managers
            managers = {
                "apt": "/usr/bin/apt",
                "apt-get": "/usr/bin/apt-get",
                "dnf": "/usr/bin/dnf",
                "yum": "/usr/bin/yum",
                "pacman": "/usr/bin/pacman",
                "zypper": "/usr/bin/zypper",
            }
            for manager, path in managers.items():
                if os.path.exists(path):
                    return manager
        elif self.os_type == "darwin":
            if os.path.exists("/usr/local/bin/brew") or os.path.exists(
                "/opt/homebrew/bin/brew"
            ):
                return "brew"
        elif self.os_type == "windows":
            return "choco"  # Chocolatey

        return "unknown"

    def is_command_available(self, command: str) -> bool:
        """Check if a command is available"""
        try:
            if self.os_type == "windows":
                result = subprocess.run(
                    ["where", command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5,
                )
            else:
                result = subprocess.run(
                    ["which", command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=5,
                )
            return result.returncode == 0
        except:
            return False

    def get_terminal_size(self) -> tuple:
        """Get terminal size (columns, lines)"""
        try:
            size = os.get_terminal_size()
            return (size.columns, size.lines)
        except:
            return (80, 24)  # Default fallback

    def is_online(self) -> bool:
        """Check if system has internet connection"""
        try:
            import socket

            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False

    def __str__(self) -> str:
        return f"OS: {self.os_type} | Version: {self.os_release} | Termux: {self.is_termux}"


class CommandExecutor:
    """Safe command execution with error handling"""

    def __init__(self, system_info: SystemInfo):
        self.system_info = system_info
        self.logger = logging.getLogger("pytools.executor")

    def run(
        self,
        command: str,
        shell: bool = True,
        check: bool = False,
        timeout: Optional[int] = None,
        capture_output: bool = False,
        sudo: bool = False,
    ) -> subprocess.CompletedProcess:
        """
        Execute a command safely

        Args:
            command: Command to execute
            shell: Use shell
            check: Raise exception on non-zero exit
            timeout: Command timeout in seconds
            capture_output: Capture stdout and stderr
            sudo: Prepend sudo to command
        """
        # Add sudo if needed and not in Termux
        if sudo and not self.system_info.is_termux and not self.system_info.is_root:
            if self.system_info.os_type != "windows":
                command = f"sudo {command}"

        try:
            self.logger.debug(f"Executing command: {command}")

            result = subprocess.run(
                command,
                shell=shell,
                check=check,
                timeout=timeout,
                capture_output=capture_output,
                text=True,
            )

            self.logger.debug(
                f"Command completed with return code: {result.returncode}"
            )
            return result

        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Command timed out: {command}")
            raise
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with code {e.returncode}: {command}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error executing command: {e}")
            raise

    def run_silent(self, command: str, timeout: Optional[int] = 5) -> bool:
        """
        Run command silently and return success status
        """
        try:
            result = self.run(command, capture_output=True, timeout=timeout)
            return result.returncode == 0
        except:
            return False

    def get_output(self, command: str, timeout: Optional[int] = 10) -> Optional[str]:
        """
        Execute command and return output
        """
        try:
            result = self.run(command, capture_output=True, timeout=timeout)
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except:
            return None


def clear_screen():
    """Clear terminal screen in a cross-platform way"""
    system_info = SystemInfo()
    if system_info.os_type == "windows":
        os.system("cls")
    else:
        os.system("clear")


def ensure_directory(path: str) -> bool:
    """Ensure directory exists, create if not"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        return False


def format_bytes(bytes_size: int) -> str:
    """Format bytes to human readable format"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def format_duration(seconds: int) -> str:
    """Format seconds to human readable duration"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def validate_url(url: str) -> bool:
    """Validate if string is a valid URL"""
    import re

    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return url_pattern.match(url) is not None


def validate_ip(ip: str) -> bool:
    """Validate if string is a valid IP address"""
    import re

    ip_pattern = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    return ip_pattern.match(ip) is not None


def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_input(prompt: str, default: str = "", timeout: Optional[int] = None) -> str:
    """Safe input with timeout and default value"""
    try:
        if timeout:
            # Simple timeout implementation
            import signal

            def timeout_handler(signum, frame):
                raise TimeoutError("Input timeout")

            if hasattr(signal, "SIGALRM"):
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout)

        user_input = input(prompt).strip()

        if timeout and hasattr(signal, "SIGALRM"):
            signal.alarm(0)

        return user_input if user_input else default
    except:
        return default
