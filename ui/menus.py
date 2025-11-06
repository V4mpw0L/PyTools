#!/usr/bin/env python3
"""
PyTools v2.0.0 - UI Menus Module
Menu system with categories and navigation
"""

from typing import Optional, List, Dict, Callable, Any
from .display import Display, ASCII3D


class MenuItem:
    """Represents a single menu item"""

    def __init__(
        self,
        number: int,
        title: str,
        description: str,
        callback: Callable,
        icon: str = "",
        color: str = "cyan",
        category: str = "general",
    ):
        self.number = number
        self.title = title
        self.description = description
        self.callback = callback
        self.icon = icon
        self.color = color
        self.category = category

    def execute(self):
        """Execute the menu item's callback"""
        return self.callback()


class MenuCategory:
    """Represents a menu category"""

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        icon: str = "",
        color: str = "cyan",
    ):
        self.name = name
        self.title = title
        self.description = description
        self.icon = icon
        self.color = color
        self.items: List[MenuItem] = []

    def add_item(self, item: MenuItem):
        """Add item to category"""
        self.items.append(item)

    def get_items(self) -> List[MenuItem]:
        """Get all items in category"""
        return self.items


class MenuManager:
    """Main menu manager"""

    def __init__(self, display: Display):
        self.display = display
        self.categories: Dict[str, MenuCategory] = {}
        self.main_menu_items: List[MenuItem] = []
        self.running = True

    def add_category(self, category: MenuCategory):
        """Add a category to the menu"""
        self.categories[category.name] = category

    def add_main_menu_item(self, item: MenuItem):
        """Add item directly to main menu"""
        self.main_menu_items.append(item)

    def show_main_menu(self):
        """Display main menu with categories"""
        self.display.clear()
        self.display.show_logo("3d")
        self.display.console.print()

        # Show version and credits
        self.display.console.print(
            "[dim]Version 2.0.0 | Created by V4mpw0L | 2024[/dim]",
            justify="center",
        )
        self.display.console.print()

        # Prepare menu options
        options = []

        # Add categories
        for i, (name, category) in enumerate(self.categories.items(), start=1):
            options.append(
                {
                    "number": str(i),
                    "icon": category.icon,
                    "title": category.title,
                    "color": category.color,
                }
            )

        # Add separator
        separator_index = len(options) + 1

        # Add extra options
        if self.main_menu_items:
            for item in self.main_menu_items:
                separator_index += 1
                options.append(
                    {
                        "number": str(separator_index),
                        "icon": item.icon,
                        "title": item.title,
                        "color": item.color,
                    }
                )

        # Add exit option
        exit_number = len(options) + 1
        options.append(
            {
                "number": str(exit_number),
                "icon": "🚪",
                "title": "Exit",
                "color": "red",
            }
        )

        # Display menu
        self.display.show_menu("🎯 MAIN MENU", options, columns=2)
        self.display.console.print()

        return exit_number

    def show_category_menu(self, category: MenuCategory):
        """Display category-specific menu"""
        self.display.clear()
        self.display.show_header(
            f"{category.icon} {category.title}", category.description
        )

        # Prepare options
        options = []
        for item in category.items:
            options.append(
                {
                    "number": str(item.number),
                    "icon": item.icon,
                    "title": item.title,
                    "color": item.color,
                }
            )

        # Add back option
        back_number = len(options) + 1
        options.append(
            {
                "number": str(back_number),
                "icon": "◀",
                "title": "Back to Main Menu",
                "color": "yellow",
            }
        )

        # Display menu
        self.display.show_menu(f"{category.icon} {category.title.upper()}", options)
        self.display.console.print()

        return back_number

    def get_user_choice(self, max_option: int) -> Optional[int]:
        """Get and validate user choice"""
        try:
            choice = self.display.prompt("Enter your choice", default="")
            if not choice:
                return None

            choice_num = int(choice)
            if 1 <= choice_num <= max_option:
                return choice_num
            else:
                self.display.show_error(
                    f"Invalid choice. Please enter a number between 1 and {max_option}"
                )
                self.display.pause()
                return None
        except ValueError:
            self.display.show_error("Invalid input. Please enter a number.")
            self.display.pause()
            return None
        except (KeyboardInterrupt, EOFError):
            self.display.console.print()
            raise KeyboardInterrupt()

    def run_main_menu(self):
        """Run the main menu loop"""
        while self.running:
            try:
                exit_number = self.show_main_menu()
                choice = self.get_user_choice(exit_number)

                if choice is None:
                    continue

                if choice == exit_number:
                    self.running = False
                    break

                # Check if it's a category
                categories_list = list(self.categories.values())
                if 1 <= choice <= len(categories_list):
                    category = categories_list[choice - 1]
                    self.run_category_menu(category)
                else:
                    # Check main menu items
                    main_item_index = choice - len(categories_list) - 1
                    if 0 <= main_item_index < len(self.main_menu_items):
                        item = self.main_menu_items[main_item_index]
                        self.execute_item(item)
            except KeyboardInterrupt:
                self.display.console.print()
                if self.display.confirm("\nExit PyTools?", default=True):
                    self.running = False
                    break

    def run_category_menu(self, category: MenuCategory):
        """Run category menu loop"""
        while self.running:
            try:
                back_number = self.show_category_menu(category)
                choice = self.get_user_choice(back_number)

                if choice is None:
                    continue

                if choice == back_number:
                    break

                # Find and execute item
                for item in category.items:
                    if item.number == choice:
                        self.execute_item(item)
                        break
            except KeyboardInterrupt:
                self.display.console.print()
                self.display.show_info("Returning to main menu...")
                break

    def execute_item(self, item: MenuItem):
        """Execute a menu item"""
        try:
            self.display.clear()
            self.display.show_section(item.title, item.icon)

            # Execute the callback
            result = item.callback()

            # Show result if any
            if result is not None:
                if isinstance(result, bool):
                    if result:
                        self.display.show_success("Operation completed successfully!")
                    else:
                        self.display.show_warning("Operation completed with warnings.")
                elif isinstance(result, str):
                    self.display.show_info(result)

        except KeyboardInterrupt:
            self.display.console.print()
            self.display.show_warning("Operation cancelled by user.")
        except Exception as e:
            self.display.show_error(f"Error: {str(e)}")
        finally:
            self.display.console.print()
            self.display.pause()

    def stop(self):
        """Stop the menu"""
        self.running = False


def create_default_categories() -> Dict[str, MenuCategory]:
    """Create default menu categories"""
    categories = {
        "system": MenuCategory(
            name="system",
            title="System Tools",
            description="System monitoring, management and maintenance",
            icon=ASCII3D.SYSTEM_ICON,
            color="cyan",
        ),
        "network": MenuCategory(
            name="network",
            title="Network Tools",
            description="Network diagnostics and information",
            icon=ASCII3D.NETWORK_ICON,
            color="blue",
        ),
        "security": MenuCategory(
            name="security",
            title="Security Tools",
            description="Security analysis and protection",
            icon=ASCII3D.SECURITY_ICON,
            color="red",
        ),
        "ip": MenuCategory(
            name="ip",
            title="IP Tools",
            description="IP address utilities and geolocation",
            icon=ASCII3D.IP_ICON,
            color="yellow",
        ),
        "downloads": MenuCategory(
            name="downloads",
            title="Download Tools",
            description="Download videos, audio, and files",
            icon=ASCII3D.DOWNLOAD_ICON,
            color="green",
        ),
        "utilities": MenuCategory(
            name="utilities",
            title="Utilities",
            description="Various utility tools",
            icon=ASCII3D.UTILITY_ICON,
            color="magenta",
        ),
        "config": MenuCategory(
            name="config",
            title="Configuration",
            description="Settings, updates and information",
            icon=ASCII3D.CONFIG_ICON,
            color="white",
        ),
    }

    return categories


def build_menu_structure(display: Display, modules: Dict[str, Any]) -> MenuManager:
    """
    Build complete menu structure with modules

    Args:
        display: Display instance
        modules: Dictionary of module instances by category

    Returns:
        Configured MenuManager
    """
    manager = MenuManager(display)

    # Create categories
    categories = create_default_categories()

    # Add categories to manager
    for category in categories.values():
        manager.add_category(category)

    # Add modules to their respective categories
    for category_name, module_list in modules.items():
        if category_name in categories:
            category = categories[category_name]
            for module in module_list:
                item = MenuItem(
                    number=len(category.items) + 1,
                    title=module.name,
                    description=module.description,
                    callback=module.execute,
                    icon=getattr(module, "icon", "▸"),
                    color=category.color,
                    category=category_name,
                )
                category.add_item(item)

    return manager
