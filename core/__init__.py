#!/usr/bin/env python3
"""
PyTools v2.0.0 - Core Module
Core functionality and base classes
"""

from .base import (
    BaseModule,
    SystemInfo,
    CommandExecutor,
    clear_screen,
    ensure_directory,
    format_bytes,
    format_duration,
    validate_url,
    validate_ip,
    get_timestamp,
    safe_input,
)

from .utils import (
    Config,
    Logger,
    Cache,
    setup_logging,
    get_config,
    get_logger,
    get_cache,
)

__all__ = [
    # Base classes
    "BaseModule",
    "SystemInfo",
    "CommandExecutor",
    # Utility functions
    "clear_screen",
    "ensure_directory",
    "format_bytes",
    "format_duration",
    "validate_url",
    "validate_ip",
    "get_timestamp",
    "safe_input",
    # Config and logging
    "Config",
    "Logger",
    "Cache",
    "setup_logging",
    "get_config",
    "get_logger",
    "get_cache",
]

__version__ = "2.0.0"
__author__ = "V4mpw0L"
__license__ = "MIT"
