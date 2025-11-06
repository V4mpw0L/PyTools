#!/usr/bin/env python3
"""
PyTools v2.0.0 - UI Display Module
Advanced terminal UI with 3D ASCII art, colors, and animations
"""

import os
import sys
import time
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
)
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.style import Style
from rich.box import ROUNDED, DOUBLE, HEAVY, MINIMAL, ASCII
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.tree import Tree
from rich.syntax import Syntax
from rich.markdown import Markdown

# Initialize console
console = Console()


class Colors:
    """Color schemes for PyTools"""

    # Gradients
    CYBER_GRADIENT = ["#00ff41", "#00cc33", "#009926", "#006619"]
    FIRE_GRADIENT = ["#ff0000", "#ff4500", "#ff8c00", "#ffd700"]
    OCEAN_GRADIENT = ["#000080", "#0000cd", "#1e90ff", "#00bfff"]
    PURPLE_GRADIENT = ["#4b0082", "#8b00ff", "#9370db", "#ba55d3"]

    # Standard colors
    PRIMARY = "#00ff41"
    SECONDARY = "#00bfff"
    SUCCESS = "#00ff00"
    WARNING = "#ffff00"
    ERROR = "#ff0000"
    INFO = "#00bfff"

    # Text colors
    TEXT_BRIGHT = "bright_white"
    TEXT_DIM = "dim white"
    TEXT_HIGHLIGHT = "bold cyan"


class ASCII3D:
    """3D ASCII Art for PyTools"""

    LOGO_3D = """
    ██████╗ ██╗   ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝        ██║   ██║   ██║██║   ██║██║     ███████╗
    ██╔═══╝   ╚██╔╝         ██║   ██║   ██║██║   ██║██║     ╚════██║
    ██║        ██║          ██║   ╚██████╔╝╚██████╔╝███████╗███████║
    ╚═╝        ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
    """

    LOGO_SLANT = r"""
       ____        ______           __
      / __ \__  __/_  __/___  ____  / /____
     / /_/ / / / / / / / __ \/ __ \/ / ___/
    / ____/ /_/ / / / / /_/ / /_/ / (__  )
   /_/    \__, / /_/  \____/\____/_/____/
         /____/
    """

    LOGO_ISOMETRIC = r"""
      ___           ___           ___           ___           ___       ___
     /\  \         /\__\         /\  \         /\  \         /\__\     /\  \
    /::\  \       /::|  |        \:\  \       /::\  \       /:/  /    /::\  \
   /:/\:\  \     /:|:|  |         \:\  \     /:/\:\  \     /:/  /    /:/\:\  \
  /::\~\:\  \   /:/|:|  |__       /::\  \   /:/  \:\  \   /:/  /    /::\~\:\  \
 /:/\:\ \:\__\ /:/ |:| /\__\     /:/\:\__\ /:/__/ \:\__\ /:/__/    /:/\:\ \:\__\
 \/__\:\/:/  / \/__|:|/:/  /    /:/  \/__/ \:\  \ /:/  / \:\  \    \/_|::\/:/  /
      \::/  /      |:/:/  /    /:/  /       \:\  /:/  /   \:\  \      |:|::/  /
      /:/  /       |::/  /     \/__/         \:\/:/  /     \:\  \     |:|\/__/
     /:/  /        /:/  /                     \::/  /       \:\__\    |:|  |
     \/__/         \/__/                       \/__/         \/__/     \|__|
    """

    BANNER = r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║  ____        _____           _                ___   ___  ___     ║
    ║ |  _ \\ _   _|_   _|__   ___ | |___  __   __ |__ \\ / _ \\/ _ \\    ║
    ║ | |_) | | | | | |/ _ \\ / _ \\| / __| \\ \\ / /    ) | | | | | |   ║
    ║ |  __/| |_| | | | (_) | (_) | \\__ \\  \\ V /    / /| |_| | |_| |   ║
    ║ |_|    \\__, | |_|\\___/ \\___/|_|___/   \\_/    |_(_)\\___(_)___/    ║
    ║        |___/                                                      ║
    ╚══════════════════════════════════════════════════════════════════╝
    """

    HEADER_SIMPLE = """
    ╔═══════════════════════════════════════╗
    ║         P Y   T O O L S   v2.0        ║
    ╚═══════════════════════════════════════╝
    """

    # Category Icons
    SYSTEM_ICON = "🖥️ "
    NETWORK_ICON = "🌐"
    SECURITY_ICON = "🔒"
    IP_ICON = "📍"
    DOWNLOAD_ICON = "📥"
    UTILITY_ICON = "🛠️ "
    CONFIG_ICON = "⚙️ "

    # Status Icons
    SUCCESS_ICON = "✓"
    ERROR_ICON = "✗"
    WARNING_ICON = "⚠"
    INFO_ICON = "ℹ"
    LOADING_ICON = "⚡"


class Display:
    """Main display manager"""

    def __init__(self, theme: str = "cyberpunk"):
        self.console = console
        self.theme = theme
        self.width = self._get_console_width()

    def _get_console_width(self) -> int:
        """Get console width"""
        try:
            return self.console.width
        except:
            return 80

    def clear(self):
        """Clear screen"""
        self.console.clear()

    def show_logo(self, style: str = "3d"):
        """Display PyTools logo"""
        self.clear()

        if style == "3d":
            logo = ASCII3D.LOGO_3D
        elif style == "slant":
            logo = ASCII3D.LOGO_SLANT
        elif style == "isometric":
            logo = ASCII3D.LOGO_ISOMETRIC
        elif style == "banner":
            logo = ASCII3D.BANNER
        else:
            logo = ASCII3D.HEADER_SIMPLE

        # Apply gradient effect
        lines = logo.split("\n")
        gradient = Colors.CYBER_GRADIENT
        total_lines = len(lines)

        for i, line in enumerate(lines):
            if line.strip():
                color_index = int((i / total_lines) * (len(gradient) - 1))
                color = gradient[color_index]
                self.console.print(line, style=f"bold {color}", justify="center")

    def show_header(self, title: str, subtitle: Optional[str] = None):
        """Show header with title"""
        panel_content = f"[bold cyan]{title}[/bold cyan]"
        if subtitle:
            panel_content += f"\n[dim]{subtitle}[/dim]"

        panel = Panel(
            Align.center(panel_content),
            box=DOUBLE,
            style="cyan",
            border_style="bright_cyan",
        )
        self.console.print(panel)
        self.console.print()

    def show_section(self, title: str, icon: str = ""):
        """Show section header"""
        text = f"{icon} {title}" if icon else title
        self.console.print()
        self.console.rule(f"[bold cyan]{text}[/bold cyan]", style="cyan")
        self.console.print()

    def show_menu(self, title: str, options: List[Dict[str, str]], columns: int = 2):
        """
        Display menu with options

        Args:
            title: Menu title
            options: List of dicts with 'number', 'icon', 'title', 'color'
            columns: Number of columns for layout
        """
        # Create table
        table = Table(
            show_header=False,
            box=None,
            padding=(0, 2),
            expand=False,
        )

        # Add columns
        for _ in range(columns):
            table.add_column(style="bold")

        # Add rows
        for i in range(0, len(options), columns):
            row_items = []
            for j in range(columns):
                if i + j < len(options):
                    opt = options[i + j]
                    num = opt.get("number", "")
                    icon = opt.get("icon", "")
                    title = opt.get("title", "")
                    color = opt.get("color", "cyan")

                    item = (
                        f"[{color}]{num}.[/{color}] [{color}]{icon} {title}[/{color}]"
                    )
                    row_items.append(item)
                else:
                    row_items.append("")

            table.add_row(*row_items)

        # Show in panel
        panel = Panel(
            table,
            title=f"[bold bright_cyan]{title}[/bold bright_cyan]",
            border_style="cyan",
            box=ROUNDED,
        )
        self.console.print(panel)

    def show_info(self, message: str, icon: bool = True):
        """Show info message"""
        icon_str = f"{ASCII3D.INFO_ICON} " if icon else ""
        self.console.print(f"[cyan]{icon_str}{message}[/cyan]")

    def show_success(self, message: str, icon: bool = True):
        """Show success message"""
        icon_str = f"{ASCII3D.SUCCESS_ICON} " if icon else ""
        self.console.print(f"[green]{icon_str}{message}[/green]")

    def show_error(self, message: str, icon: bool = True):
        """Show error message"""
        icon_str = f"{ASCII3D.ERROR_ICON} " if icon else ""
        self.console.print(f"[red]{icon_str}{message}[/red]")

    def show_warning(self, message: str, icon: bool = True):
        """Show warning message"""
        icon_str = f"{ASCII3D.WARNING_ICON} " if icon else ""
        self.console.print(f"[yellow]{icon_str}{message}[/yellow]")

    def show_box(self, message: str, title: str = "", style: str = "cyan"):
        """Show message in a box"""
        panel = Panel(
            message,
            title=title,
            border_style=style,
            box=ROUNDED,
        )
        self.console.print(panel)

    def show_table(
        self,
        title: str,
        headers: List[str],
        rows: List[List[str]],
        colors: Optional[List[str]] = None,
    ):
        """Display data in a table"""
        table = Table(
            title=title,
            show_header=True,
            header_style="bold cyan",
            box=ROUNDED,
            border_style="cyan",
        )

        # Add columns
        for i, header in enumerate(headers):
            style = colors[i] if colors and i < len(colors) else None
            table.add_column(header, style=style)

        # Add rows
        for row in rows:
            table.add_row(*[str(cell) for cell in row])

        self.console.print(table)

    def show_key_value(self, data: Dict[str, str], title: str = ""):
        """Display key-value pairs"""
        table = Table(
            show_header=False,
            box=MINIMAL,
            border_style="cyan",
            title=title if title else None,
        )

        table.add_column("Key", style="cyan bold")
        table.add_column("Value", style="bright_white")

        for key, value in data.items():
            table.add_row(key, str(value))

        self.console.print(table)

    def show_progress_bar(self, total: int, description: str = "Processing..."):
        """Create and return a progress bar context"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(complete_style="cyan", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=self.console,
        )

    def show_spinner(self, text: str = "Loading..."):
        """Show spinner animation"""
        from rich.spinner import Spinner

        spinner = Spinner("dots", text=text, style="cyan")
        return spinner

    def show_tree(self, root_label: str, data: Dict[str, Any]):
        """Display hierarchical data as tree"""
        tree = Tree(f"[bold cyan]{root_label}[/bold cyan]")

        def add_items(parent, items):
            for key, value in items.items():
                if isinstance(value, dict):
                    branch = parent.add(f"[yellow]{key}[/yellow]")
                    add_items(branch, value)
                else:
                    parent.add(f"[cyan]{key}:[/cyan] [white]{value}[/white]")

        add_items(tree, data)
        self.console.print(tree)

    def prompt(self, message: str, default: str = "", password: bool = False) -> str:
        """Prompt user for input"""
        from rich.prompt import Prompt

        if password:
            from rich.prompt import Prompt

            return Prompt.ask(f"[cyan]{message}[/cyan]", password=True, default=default)
        return Prompt.ask(f"[cyan]{message}[/cyan]", default=default)

    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask user for confirmation"""
        from rich.prompt import Confirm

        return Confirm.ask(f"[yellow]{message}[/yellow]", default=default)

    def show_credits(self, version: str = "2.0.0", author: str = "V4mpw0L"):
        """Display credits"""
        credits_text = f"""
[bold cyan]PyTools v{version}[/bold cyan]
[dim]A powerful Python toolkit for system management[/dim]

[bold yellow]Created by:[/bold yellow] [red]{author}[/red]
[bold yellow]Year:[/bold yellow] 2024
[bold yellow]License:[/bold yellow] MIT

[dim]Made with ❤️  and Python 🐍[/dim]
        """

        panel = Panel(
            Align.center(credits_text.strip()),
            box=DOUBLE,
            border_style="magenta",
            style="on black",
        )
        self.console.print(panel)

    def show_divider(self, char: str = "─", style: str = "cyan"):
        """Show divider line"""
        self.console.print(char * self.width, style=style)

    def pause(self, message: str = "Press Enter to continue..."):
        """Pause and wait for user input"""
        self.console.print()
        self.console.print(f"[dim cyan]{message}[/dim cyan]", end="")
        input()

    def animate_text(self, text: str, delay: float = 0.03):
        """Animate text character by character"""
        for char in text:
            self.console.print(char, end="", style="cyan")
            time.sleep(delay)
        self.console.print()


def create_display(theme: str = "cyberpunk") -> Display:
    """Create and return display instance"""
    return Display(theme)


def show_startup_animation():
    """Show startup animation"""
    display = Display()
    display.clear()

    # Show logo with animation
    display.show_logo("3d")

    # Show loading message
    with display.show_progress_bar(100, "Initializing PyTools...") as progress:
        task = progress.add_task("", total=100)
        for i in range(100):
            time.sleep(0.01)
            progress.update(task, advance=1)

    time.sleep(0.3)


def show_goodbye_message():
    """Show goodbye message"""
    display = Display()
    display.console.print()
    display.show_box(
        "[bold cyan]Thanks for using PyTools![/bold cyan]\n[dim]See you soon! 👋[/dim]",
        title="Goodbye",
        style="magenta",
    )
    display.console.print()
