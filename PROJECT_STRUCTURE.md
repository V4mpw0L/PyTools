# PyTools v2.0.0 - Project Structure 📁

Complete guide to the modular architecture and file organization.

---

## 📂 Directory Tree

```
PyTools/
├── 📄 pytools.py                 # Main application entry point
├── 📄 install.sh                 # Automated installation script
├── 📄 requirements.txt           # Python dependencies
├── 📄 LICENSE.txt                # MIT License
├── 📄 .gitignore                 # Git ignore rules
│
├── 📚 Documentation/
│   ├── README.md                 # Main documentation (GitHub)
│   ├── QUICKSTART.md             # Quick start guide
│   ├── CHANGELOG.md              # Version history
│   ├── UPGRADE_SUMMARY.md        # v1 to v2 upgrade details
│   └── PROJECT_STRUCTURE.md      # This file
│
├── 🏗️ core/                      # Core architecture
│   ├── __init__.py               # Core exports
│   ├── base.py                   # Base classes and utilities
│   │   ├── BaseModule            # Abstract base for all modules
│   │   ├── SystemInfo            # System detection (singleton)
│   │   ├── CommandExecutor       # Safe command execution
│   │   └── Utility functions     # format_bytes, validate_ip, etc.
│   │
│   └── utils.py                  # Configuration and logging
│       ├── Config                # YAML configuration manager
│       ├── Logger                # Rotating log system
│       └── Cache                 # Simple cache manager
│
├── 🎨 ui/                        # User interface
│   ├── __init__.py               # UI exports
│   ├── display.py                # Display and rendering
│   │   ├── Display               # Main display class
│   │   ├── Colors                # Color schemes
│   │   ├── ASCII3D               # 3D ASCII art
│   │   └── Rendering methods     # Tables, panels, progress bars
│   │
│   └── menus.py                  # Menu system
│       ├── MenuItem              # Single menu item
│       ├── MenuCategory          # Category container
│       └── MenuManager           # Menu orchestrator
│
├── 🛠️ modules/                   # Tool implementations
│   ├── __init__.py               # Module factory
│   │
│   ├── system.py                 # System Tools (7 modules)
│   │   ├── SystemInformationModule
│   │   ├── SystemUptimeModule
│   │   ├── DiskUsageModule
│   │   ├── MemoryUsageModule
│   │   ├── ProcessListModule
│   │   ├── SystemUpdateModule
│   │   └── SystemCleanModule
│   │
│   ├── network.py                # Network Tools (7 modules)
│   │   ├── NetworkInfoModule
│   │   ├── PingModule
│   │   ├── TracerouteModule
│   │   ├── PortScannerModule
│   │   ├── SpeedTestModule
│   │   ├── DNSLookupModule
│   │   └── WHOISLookupModule
│   │
│   ├── security.py               # Security Tools (5 modules)
│   │   ├── PasswordStrengthModule
│   │   ├── PasswordGeneratorModule
│   │   ├── HashGeneratorModule
│   │   ├── MalwareScanModule
│   │   └── FileEncryptionModule
│   │
│   ├── ip_tools.py               # IP Tools (3 modules)
│   │   ├── GeolocateIPModule
│   │   ├── MyPublicIPModule
│   │   └── IPCalculatorModule
│   │
│   ├── downloads.py              # Download Tools (3 modules)
│   │   ├── YouTubeDownloadModule
│   │   ├── FileDownloaderModule
│   │   └── BatchDownloaderModule
│   │
│   └── utilities.py              # Utilities (5 modules)
│       ├── TempEmailModule
│       ├── QRCodeGeneratorModule
│       ├── TextEncoderModule
│       ├── JSONFormatterModule
│       └── UUIDGeneratorModule
│
├── ⚙️ config/                    # Configuration
│   └── config.yaml               # Default configuration template
│
└── 🗄️ old_v1_backup/            # Archived v1 files
    ├── README.md                 # Backup folder info
    ├── pytools_old_v1.py.bak     # Original v1 script
    ├── requirements_old_v1.txt.bak
    └── README_old_v1.md.bak
```

---

## 🏗️ Architecture Overview

### Layer 1: Core Foundation
**Location**: `core/`

The foundation layer provides base classes, utilities, and system-level functionality.

#### Key Components:

**`base.py`** (346 lines)
- `BaseModule`: Abstract base class for all tools
- `SystemInfo`: Singleton for system detection
- `CommandExecutor`: Safe command execution with timeouts
- Utility functions: format_bytes, validate_ip, etc.

**`utils.py`** (299 lines)
- `Config`: YAML configuration manager
- `Logger`: Rotating file logger with levels
- `Cache`: Memory and persistent cache system

### Layer 2: User Interface
**Location**: `ui/`

The presentation layer handles all visual output and user interaction.

#### Key Components:

**`display.py`** (440 lines)
- `Display`: Main display manager
- `Colors`: Color schemes and gradients
- `ASCII3D`: 3D ASCII art logos
- Methods: tables, panels, progress bars, prompts

**`menus.py`** (370 lines)
- `MenuItem`: Single menu option
- `MenuCategory`: Group of related items
- `MenuManager`: Menu navigation and execution

### Layer 3: Business Logic
**Location**: `modules/`

The business layer contains all tool implementations organized by category.

#### Module Categories:

1. **System Tools** (`system.py` - 580 lines)
   - System monitoring and management
   - 7 tools for system operations

2. **Network Tools** (`network.py` - 477 lines)
   - Network diagnostics and testing
   - 7 tools for network operations

3. **Security Tools** (`security.py` - 492 lines)
   - Security analysis and protection
   - 5 tools for security operations

4. **IP Tools** (`ip_tools.py` - 355 lines)
   - IP address utilities
   - 3 tools for IP operations

5. **Download Tools** (`downloads.py` - 381 lines)
   - File and media downloads
   - 3 tools for download operations

6. **Utilities** (`utilities.py` - 397 lines)
   - Various utility tools
   - 5 miscellaneous tools

### Layer 4: Configuration
**Location**: `config/`

User preferences and settings in YAML format.

---

## 🔄 Data Flow

```
User Input
    ↓
pytools.py (Main Entry)
    ↓
MenuManager (ui/menus.py)
    ↓
MenuItem.execute()
    ↓
Module.execute() (modules/*.py)
    ↓
Display.show_*() (ui/display.py)
    ↓
Console Output
```

---

## 📦 Module Creation Pattern

Every tool follows this pattern:

```python
from core.base import BaseModule
from ui.display import Display

class MyToolModule(BaseModule):
    def __init__(self, display: Display):
        super().__init__(
            name="My Tool",
            description="Does something cool",
            category="utilities"
        )
        self.display = display
        self.icon = "🔧"
    
    def execute(self) -> bool:
        try:
            # Tool implementation
            self.display.show_info("Working...")
            # Do stuff
            self.display.show_success("Done!")
            return True
        except Exception as e:
            self.log_error("Failed", e)
            self.display.show_error(f"Error: {e}")
            return False
```

---

## 🗂️ File Purposes

### Core Files

| File | Lines | Purpose |
|------|-------|---------|
| `pytools.py` | 390 | Main application, initialization, config modules |
| `core/base.py` | 346 | Base classes, system detection, utilities |
| `core/utils.py` | 299 | Configuration, logging, caching |

### UI Files

| File | Lines | Purpose |
|------|-------|---------|
| `ui/display.py` | 440 | Terminal rendering, colors, ASCII art |
| `ui/menus.py` | 370 | Menu system, navigation, execution |

### Module Files

| File | Lines | Tools | Purpose |
|------|-------|-------|---------|
| `modules/system.py` | 580 | 7 | System monitoring & management |
| `modules/network.py` | 477 | 7 | Network diagnostics |
| `modules/security.py` | 492 | 5 | Security tools |
| `modules/ip_tools.py` | 355 | 3 | IP utilities |
| `modules/downloads.py` | 381 | 3 | Download managers |
| `modules/utilities.py` | 397 | 5 | Miscellaneous tools |

### Configuration Files

| File | Purpose |
|------|---------|
| `config/config.yaml` | Default settings template |
| `~/.config/pytools/config.yaml` | User configuration (created at runtime) |
| `~/.config/pytools/pytools.log` | Application logs (rotating) |

---

## 🎯 Design Patterns Used

### 1. **Singleton Pattern**
- `SystemInfo`: Single instance for system detection
- `Config`: Single configuration instance
- `Logger`: Single logging instance

### 2. **Factory Pattern**
- `get_all_modules()`: Creates all tool modules
- `build_menu_structure()`: Builds menu from modules

### 3. **Strategy Pattern**
- Different package managers (apt, dnf, yum, etc.)
- Multiple API providers with fallbacks
- Cross-platform command execution

### 4. **Template Method Pattern**
- `BaseModule.execute()`: Template for all tools
- Consistent error handling and logging

### 5. **Facade Pattern**
- `Display`: Simplifies Rich library complexity
- `MenuManager`: Simplifies menu operations

---

## 🚀 Adding a New Tool

To add a new tool to PyTools:

1. **Choose a category** (or create new in `modules/`)

2. **Create module class**:
```python
class MyNewToolModule(BaseModule):
    def __init__(self, display: Display):
        super().__init__(
            name="My New Tool",
            description="What it does",
            category="utilities"
        )
        self.display = display
        self.icon = "🆕"
    
    def execute(self) -> bool:
        # Implementation
        pass
```

3. **Add to module list** in `modules/utilities.py`:
```python
def get_utility_modules(display: Display) -> List[BaseModule]:
    return [
        # ... existing modules
        MyNewToolModule(display),
    ]
```

4. **Test**: Run `python3 pytools.py`

That's it! The menu system automatically detects and displays your new tool.

---

## 📊 Code Statistics

- **Total Files**: 25+
- **Total Lines**: 5000+
- **Python Files**: 18
- **Documentation**: 7 files (1700+ lines)
- **Classes**: 40+
- **Functions**: 150+
- **Tools**: 34+

---

## 🔍 Dependencies by Layer

### Core Layer
- `psutil` - System information
- `pyyaml` - Configuration
- Standard library (os, sys, platform, etc.)

### UI Layer
- `rich` - Terminal formatting
- Standard library (time, etc.)

### Module Layer
- `requests` - HTTP requests
- `speedtest-cli` - Speed testing (optional)
- `yt-dlp` / `pytube` - YouTube downloads (optional)
- `qrcode` - QR generation (optional)
- `tqdm` - Progress bars (optional)

---

## 📝 Configuration Hierarchy

1. **Default Config**: `config/config.yaml` (template)
2. **User Config**: `~/.config/pytools/config.yaml` (created on first run)
3. **Runtime Override**: Can be modified via Settings menu

---

## 🔐 Security Considerations

- ✅ No hardcoded credentials
- ✅ Input validation throughout
- ✅ Safe command execution with timeouts
- ✅ Path sanitization
- ✅ Sudo confirmation for dangerous operations
- ✅ Secure password generation using `secrets`
- ✅ XOR encryption (basic, not production-grade)

---

## 🧪 Testing Strategy

While unit tests are not yet implemented, the architecture is designed for testability:

- **BaseModule**: Can be mocked for testing
- **Display**: Can be replaced with test display
- **Config**: Can use test configuration
- **Each module**: Independent and testable

Future: Add `tests/` directory with pytest framework.

---

## 📚 Further Reading

- **README.md**: User documentation and features
- **QUICKSTART.md**: Getting started guide
- **CHANGELOG.md**: Version history
- **UPGRADE_SUMMARY.md**: v1 to v2 migration details

---

## 🤝 Contributing

When contributing new features:

1. Follow the existing architecture patterns
2. Add type hints
3. Include docstrings
4. Handle errors gracefully
5. Update documentation
6. Test on multiple platforms

---

## 📧 Contact

- **Author**: V4mpw0L
- **Year**: 2025
- **License**: MIT
- **GitHub**: https://github.com/V4mpw0L/PyTools

---

**PyTools v2.0.0 - Modular, Beautiful, Powerful** 🚀