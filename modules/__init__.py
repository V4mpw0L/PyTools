#!/usr/bin/env python3
"""
PyTools v2.0.0 - Modules Package
All tool modules organized by category
"""

from typing import Dict, List
from core.base import BaseModule
from ui.display import Display

# Import module getters
from .system import get_system_modules
from .network import get_network_modules
from .security import get_security_modules
from .ip_tools import get_ip_modules
from .downloads import get_download_modules
from .utilities import get_utility_modules


def get_all_modules(display: Display) -> Dict[str, List[BaseModule]]:
    """
    Get all modules organized by category

    Args:
        display: Display instance for UI

    Returns:
        Dictionary mapping category names to lists of modules
    """
    modules = {
        "system": get_system_modules(display),
        "network": get_network_modules(display),
        "security": get_security_modules(display),
        "ip": get_ip_modules(display),
        "downloads": get_download_modules(display),
        "utilities": get_utility_modules(display),
    }

    return modules


def get_module_count() -> int:
    """Get total number of modules"""
    from .system import get_system_modules
    from .network import get_network_modules
    from .security import get_security_modules
    from .ip_tools import get_ip_modules
    from .downloads import get_download_modules
    from .utilities import get_utility_modules

    # Create dummy display for counting
    from ui.display import Display

    display = Display()

    total = 0
    total += len(get_system_modules(display))
    total += len(get_network_modules(display))
    total += len(get_security_modules(display))
    total += len(get_ip_modules(display))
    total += len(get_download_modules(display))
    total += len(get_utility_modules(display))

    return total


__all__ = [
    "get_all_modules",
    "get_module_count",
    "get_system_modules",
    "get_network_modules",
    "get_security_modules",
    "get_ip_modules",
    "get_download_modules",
    "get_utility_modules",
]
