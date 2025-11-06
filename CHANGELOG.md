# Changelog

All notable changes to PyTools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2024-12-XX

### 🎉 MAJOR RELEASE - Complete Rewrite

This is a complete rewrite of PyTools with a focus on modularity, maintainability, and user experience.

### ✨ Added

#### **Architecture & Structure**
- Modular architecture with separated concerns
- Object-oriented design with base classes
- Proper Python package structure (core/, modules/, ui/, config/)
- Factory pattern for module creation
- Singleton pattern for configuration and system info
- Comprehensive error handling throughout

#### **User Interface**
- 3D ASCII art logo with gradient colors
- Category-based menu system with sub-menus
- Rich library integration for beautiful terminal output
- Animated progress bars with ETA
- Color-coded status messages
- Visual bars for disk and memory usage
- Table-based displays for structured data
- Panels and boxes for organized information
- Startup and goodbye animations

#### **New Tools - System (2 new)**
- **System Clean**: Clean temporary files, caches, and logs
- **Enhanced System Information**: More detailed info with psutil

#### **New Tools - Network (4 new)**
- **Port Scanner**: Scan common ports on any host
- **Internet Speed Test**: Test download/upload speeds
- **DNS Lookup**: Resolve domain names with detailed records
- **WHOIS Lookup**: Get domain registration information

#### **New Tools - Security (3 new)**
- **Password Generator**: Generate secure random passwords
- **Hash Generator**: Generate MD5, SHA1, SHA256, SHA512 hashes
- **File Encryption**: Simple XOR-based file encryption/decryption

#### **New Tools - IP Tools (2 new)**
- **My Public IP**: Display your public IP with detailed info
- **IP Calculator**: Calculate subnet information and IP ranges

#### **New Tools - Downloads (2 new)**
- **File Downloader**: Download files from direct URLs with progress
- **Batch Downloader**: Download multiple files from URL list

#### **New Tools - Utilities (5 new)**
- **QR Code Generator**: Generate QR codes from text/URLs
- **Text Encoder/Decoder**: Base64, Hex, URL encoding/decoding
- **JSON/YAML Formatter**: Format, validate, and convert JSON/YAML
- **UUID Generator**: Generate unique identifiers
- **Enhanced Temporary Email**: Better UI with real-time updates

#### **New Tools - Configuration (4 new)**
- **Update PyTools**: Update script from GitHub with safety checks
- **Settings Manager**: Configure PyTools preferences
- **Log Viewer**: View PyTools log files
- **About/Credits**: Comprehensive information and credits

#### **Configuration System**
- YAML-based configuration file
- Persistent settings across sessions
- Configurable paths for downloads
- Customizable timeouts and limits
- Theme support (foundation for future themes)
- Log rotation settings
- Cache management options

#### **Cross-Platform Support**
- Enhanced Windows support
- macOS support with Homebrew
- Android/Termux optimization
- Multi-distro Linux support (Debian, Fedora, Arch, etc.)
- Automatic package manager detection (apt, dnf, yum, pacman, brew, pkg)

#### **System Detection**
- Automatic OS detection
- Package manager detection
- Root/admin privilege detection
- Termux environment detection
- Command availability checking
- Terminal size detection
- Internet connectivity check

#### **Error Handling & Logging**
- Comprehensive exception handling
- Rotating log files with size limits
- Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Detailed error messages with context
- Graceful degradation when optional dependencies missing
- Fallback mechanisms for unavailable commands

#### **Performance**
- Caching system for API responses
- Optimized imports (lazy loading where possible)
- Parallel operations support (foundation)
- Progress tracking for long operations

### 🔄 Changed

#### **Core Improvements**
- Rewrote all 15 original tools with better error handling
- Improved system update with multi-distro support
- Enhanced ping with better output formatting
- Better IP geolocation with multiple API fallbacks
- Improved disk usage with visual progress bars
- Enhanced memory usage with swap information
- Better process listing with sorting and filtering
- Improved network info with psutil integration
- Enhanced system information display
- Better malware scanning with multiple tool support
- Improved password strength checker with detailed analysis
- Enhanced traceroute with better output
- Completely rewritten YouTube downloader with yt-dlp support
- Better temporary email with improved monitoring

#### **Dependencies**
- Upgraded to Rich library for terminal UI
- Added psutil for better system information
- Added PyYAML for configuration
- Made many dependencies optional
- Better dependency checking on startup
- Clear installation instructions for missing packages

#### **Code Quality**
- Type hints throughout codebase
- Docstrings for all classes and functions
- Consistent naming conventions
- PEP 8 compliance
- Modular and testable code structure
- Separated UI from business logic
- Reusable base classes and utilities

### 🐛 Fixed

- Fixed YouTube download issues with pytube deprecation
- Fixed ping command compatibility across platforms
- Fixed neofetch dependency issues on minimal systems
- Fixed memory calculation errors
- Fixed disk usage display on systems with many partitions
- Fixed process listing on Windows
- Fixed network interface detection issues
- Fixed temporary email API changes
- Fixed Git update conflicts
- Fixed colorama compatibility issues
- Fixed lolcat dependency on non-Unix systems
- Fixed figlet requirement making it optional
- Fixed terminal size detection failures
- Fixed encoding issues in logs
- Fixed path handling on Windows
- Fixed permission errors with better error messages

### 🗑️ Deprecated

- Old monolithic pytools.py structure (preserved as pytools.py for compatibility)
- Direct colorama usage (replaced with Rich)
- alive-progress direct usage (integrated into Display class)
- Hard-coded color schemes (moved to Colors class)
- Global variables (replaced with classes and configuration)

### 🔒 Security

- Secure password generation using secrets module
- Better input validation throughout
- Sanitized file paths to prevent directory traversal
- Secure temporary file handling
- No hardcoded credentials or API keys
- Safe command execution with timeout
- Optional sudo confirmation for dangerous operations

### 📚 Documentation

- Comprehensive README with installation guide
- Detailed tool descriptions
- Configuration documentation
- Contributing guidelines
- Code comments and docstrings
- Example usage for each tool
- Troubleshooting section
- FAQ (coming soon)

### ⚠️ Breaking Changes

- New file structure (migration needed for custom modifications)
- Configuration file moved to platform-specific location
- Download paths changed (configurable in config.yaml)
- Some command-line arguments changed (if used programmatically)
- Requires Python 3.7+ (dropped 3.6 support)
- New requirements.txt (install with pip install -r requirements_v2.txt)

### 🔄 Migration Guide (v1.0.1 → v2.0.0)

1. **Backup your current installation**
   ```bash
   cp -r PyTools PyTools_backup
   ```

2. **Pull latest changes**
   ```bash
   cd PyTools
   git pull origin main
   ```

3. **Install new dependencies**
   ```bash
   pip install -r requirements_v2.txt
   ```

4. **Run new version**
   ```bash
   python3 pytools_v2.py
   ```

5. **Configure settings (optional)**
   - Edit `~/.config/pytools/config.yaml` on Linux/macOS
   - Edit `%APPDATA%/PyTools/config.yaml` on Windows

### 📊 Statistics

- **Total Files**: 20+ Python files
- **Lines of Code**: 5000+
- **Total Tools**: 34 (was 15)
- **New Tools**: 19
- **Categories**: 7 (was 1 flat menu)
- **Supported Platforms**: 6
- **Dependencies**: 8 required, 6 optional (was 8 required)

---

## [1.0.1] - 2024-01-XX

### Added
- Initial public release
- 15 system management tools
- Basic menu system
- YouTube video/audio download
- Temporary email functionality
- System information display
- Network diagnostics
- Security tools

### Fixed
- Minor bug fixes
- Dependency issues

---

## [1.0.0] - 2024-01-XX

### Added
- Initial release
- Core functionality
- Basic tools

---

## Legend

- ✨ **Added**: New features
- 🔄 **Changed**: Changes in existing functionality
- 🐛 **Fixed**: Bug fixes
- 🗑️ **Deprecated**: Soon-to-be removed features
- 🔒 **Security**: Security improvements
- ⚠️ **Breaking**: Breaking changes

---

## Links

- [GitHub Repository](https://github.com/V4mpw0L/PyTools)
- [Issue Tracker](https://github.com/V4mpw0L/PyTools/issues)
- [Discussions](https://github.com/V4mpw0L/PyTools/discussions)

---

**Note**: Version 2.0.0 represents a complete rewrite of PyTools. While backward compatibility is maintained where possible, users are encouraged to review the migration guide and update their workflows accordingly.