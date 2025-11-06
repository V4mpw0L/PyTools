#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  ____        _____           _                ___   ___  ___     ║
║ |  _ \\ _   _|_   _|__   ___ | |___  __   __ |__ \\ / _ \\/ _ \\    ║
║ | |_) | | | | | |/ _ \\ / _ \\| / __| \\ \\ / /    ) | | | | | |   ║
║ |  __/| |_| | | | (_) | (_) | \\__ \\  \\ V /    / /| |_| | |_| |   ║
║ |_|    \\__, | |_|\\___/ \\___/|_|___/   \\_/    |_(_)\\___(_)___/    ║
║        |___/                                                      ║
╚══════════════════════════════════════════════════════════════════╝

PyTools v2.0.0 - Advanced Python Toolkit for System Management

A comprehensive, modular Python toolkit for system administration,
network diagnostics, security analysis, and various utilities.

Author: V4mpw0L
Year: 2025
License: MIT

Features:
- 🖥️  System monitoring and management
- 🌐 Network diagnostics and tools
- 🔒 Security analysis and protection
- 📍 IP address utilities
- 📥 Download managers (YouTube, files)
- 🛠️  Various utility tools
- 🎨 Beautiful 3D ASCII art interface
- 🚀 Cross-platform support (Linux, macOS, Windows, Termux)
"""

import sys
import os
import signal
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Version information
__version__ = "2.0.0"
__author__ = "V4mpw0L"
__license__ = "MIT"


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: PyTools requires Python 3.7 or higher")
        print(f"Current version: {sys.version}")
        sys.exit(1)


def check_dependencies():
    """Check and report missing dependencies"""
    required = {
        "rich": "pip install rich",
        "requests": "pip install requests",
        "psutil": "pip install psutil",
        "yaml": "pip install pyyaml",
    }

    optional = {
        "speedtest": "pip install speedtest-cli",
        "yt_dlp": "pip install yt-dlp",
        "pytube": "pip install pytube",
        "qrcode": "pip install qrcode[pil]",
        "tqdm": "pip install tqdm",
    }

    missing_required = []
    missing_optional = []

    for module, install_cmd in required.items():
        try:
            __import__(module)
        except ImportError:
            missing_required.append((module, install_cmd))

    for module, install_cmd in optional.items():
        try:
            __import__(module)
        except ImportError:
            missing_optional.append((module, install_cmd))

    if missing_required:
        print("❌ Missing required dependencies:")
        for module, cmd in missing_required:
            print(f"   • {module}: {cmd}")
        print("\nPlease install required dependencies and try again.")
        sys.exit(1)

    if missing_optional:
        print("⚠️  Optional dependencies not installed (some features may be limited):")
        for module, cmd in missing_optional:
            print(f"   • {module}: {cmd}")
        print("\nPress Enter to continue...")
        input()


def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown"""

    def signal_handler(sig, frame):
        print("\n\n👋 Interrupted by user. Exiting gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, signal_handler)


def initialize_pytools():
    """Initialize PyTools environment"""
    # Import core modules
    from core import setup_logging, get_config, SystemInfo
    from ui import Display

    # Setup logging
    logger = setup_logging()
    logger.info("PyTools v2.0.0 starting...")

    # Load configuration
    config = get_config()

    # Detect system
    system_info = SystemInfo()
    logger.info(f"System detected: {system_info}")

    # Create display
    theme = config.get("theme", "cyberpunk")
    display = Display(theme=theme)

    return display, config, system_info, logger


def create_config_modules(display):
    """Create configuration and management modules"""
    from core.base import BaseModule
    from ui import show_goodbye_message
    from core.utils import get_config, get_logger, get_cache

    class UpdateScriptModule(BaseModule):
        """Update PyTools from GitHub"""

        def __init__(self, display):
            super().__init__(
                name="Update PyTools",
                description="Update script from GitHub repository",
                category="config",
            )
            self.display = display
            self.icon = "🔄"

        def execute(self) -> bool:
            try:
                import subprocess

                self.display.show_warning(
                    "This will update PyTools from the GitHub repository"
                )

                if not self.display.confirm("Continue with update?", default=False):
                    self.display.show_warning("Update cancelled")
                    return False

                self.display.console.print()
                self.display.show_info("Fetching updates from GitHub...")

                commands = [
                    ("git fetch origin", "Fetching changes..."),
                    ("git reset --hard origin/main", "Resetting to latest version..."),
                    ("git pull origin main", "Pulling updates..."),
                ]

                for cmd, desc in commands:
                    self.display.show_info(desc)
                    try:
                        subprocess.run(cmd, shell=True, check=True, timeout=30)
                    except Exception as e:
                        self.display.show_error(f"Failed: {str(e)}")
                        return False

                self.display.console.print()
                self.display.show_success("Update completed successfully!")
                self.display.show_warning(
                    "Please restart PyTools for changes to take effect"
                )

                return True

            except Exception as e:
                self.log_error("Update failed", e)
                self.display.show_error(f"Update failed: {str(e)}")
                return False

    class SettingsModule(BaseModule):
        """Configure PyTools settings"""

        def __init__(self, display):
            super().__init__(
                name="Settings",
                description="Configure PyTools settings and preferences",
                category="config",
            )
            self.display = display
            self.icon = "⚙️"

        def execute(self) -> bool:
            try:
                config = get_config()

                self.display.show_section("Current Settings")

                settings = {
                    "Theme": config.get("theme", "cyberpunk"),
                    "Auto Update": str(config.get("auto_update", True)),
                    "Log Level": config.get("log_level", "INFO"),
                    "Show Animations": str(config.get("show_animations", True)),
                }

                self.display.show_key_value(settings, "⚙️ Configuration")

                self.display.console.print()

                if self.display.confirm("Reset to default settings?", default=False):
                    config.reset()
                    self.display.show_success("Settings reset to defaults")

                return True

            except Exception as e:
                self.log_error("Settings failed", e)
                self.display.show_error(f"Settings failed: {str(e)}")
                return False

    class ViewLogsModule(BaseModule):
        """View PyTools logs"""

        def __init__(self, display):
            super().__init__(
                name="View Logs",
                description="View PyTools log files",
                category="config",
            )
            self.display = display
            self.icon = "📋"

        def execute(self) -> bool:
            try:
                config = get_config()
                log_file = os.path.join(config.config_dir, "pytools.log")

                if not os.path.exists(log_file):
                    self.display.show_warning("No log file found")
                    return False

                self.display.show_info(f"Log file: {log_file}")
                self.display.console.print()

                # Show last 50 lines
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    last_lines = lines[-50:] if len(lines) > 50 else lines

                    for line in last_lines:
                        self.display.console.print(line.rstrip())

                return True

            except Exception as e:
                self.log_error("View logs failed", e)
                self.display.show_error(f"Failed to view logs: {str(e)}")
                return False

    class AboutModule(BaseModule):
        """About PyTools"""

        def __init__(self, display):
            super().__init__(
                name="About / Credits",
                description="About PyTools and credits",
                category="config",
            )
            self.display = display
            self.icon = "ℹ️"

        def execute(self) -> bool:
            try:
                from modules import get_module_count

                self.display.show_credits(__version__, __author__)
                self.display.console.print()

                info = {
                    "Version": __version__,
                    "Author": __author__,
                    "License": __license__,
                    "Total Modules": str(get_module_count()),
                    "Python Version": sys.version.split()[0],
                }

                self.display.show_key_value(info, "📊 Information")

                self.display.console.print()
                self.display.show_info(
                    "🌟 Star on GitHub: https://github.com/V4mpw0L/PyTools"
                )
                self.display.show_info(
                    "🐛 Report issues: https://github.com/V4mpw0L/PyTools/issues"
                )

                return True

            except Exception as e:
                self.log_error("About failed", e)
                self.display.show_error(f"Failed to show about: {str(e)}")
                return False

    return [
        UpdateScriptModule(display),
        SettingsModule(display),
        ViewLogsModule(display),
        AboutModule(display),
    ]


def main():
    """Main entry point for PyTools"""
    try:
        # Check Python version
        check_python_version()

        # Setup signal handlers
        setup_signal_handlers()

        # Check dependencies
        check_dependencies()

        # Initialize PyTools
        display, config, system_info, logger = initialize_pytools()

        # Show startup animation
        from ui import show_startup_animation

        if config.get("show_animations", True):
            show_startup_animation()
        else:
            display.clear()
            display.show_logo("3d")

        # Import modules
        from modules import get_all_modules
        from ui import build_menu_structure

        # Get all tool modules
        modules = get_all_modules(display)

        # Add config modules
        modules["config"] = create_config_modules(display)

        # Build menu structure
        menu_manager = build_menu_structure(display, modules)

        logger.info("PyTools initialized successfully")

        # Run main menu
        menu_manager.run_main_menu()

        # Show goodbye message
        from ui import show_goodbye_message

        display.clear()
        show_goodbye_message()

        logger.info("PyTools exited normally")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
