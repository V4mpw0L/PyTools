# PyTools v2.0.0 🚀

<div align="center">

```
    ██████╗ ██╗   ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝        ██║   ██║   ██║██║   ██║██║     ███████╗
    ██╔═══╝   ╚██╔╝         ██║   ██║   ██║██║   ██║██║     ╚════██║
    ██║        ██║          ██║   ╚██████╔╝╚██████╔╝███████╗███████║
    ╚═╝        ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
```

**Advanced Python Toolkit for System Management**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/V4mpw0L/PyTools)

*Complete rewrite with modular architecture, beautiful 3D ASCII UI, and 34+ tools!*

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [What's New in v2.0.0](#-whats-new-in-v200)
- [Installation](#-installation)
- [Usage](#-usage)
- [Tool Categories](#-tool-categories)
- [Configuration](#-configuration)
- [Screenshots](#-screenshots)
- [Compatibility](#-compatibility)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## 🌟 Overview

**PyTools** is a comprehensive, modular Python toolkit designed for system administrators, developers, and power users. It provides 34+ tools organized into 7 categories, featuring a beautiful terminal UI with 3D ASCII art, cross-platform support, and robust error handling.

### Key Highlights

- 🎨 **Beautiful UI**: 3D ASCII art, gradient colors, animated progress bars
- 🔧 **34+ Tools**: System monitoring, network diagnostics, security analysis, and more
- 📦 **Modular Architecture**: Clean, maintainable code with separated concerns
- 🌍 **Cross-Platform**: Linux, macOS, Windows, Android (Termux)
- 🔒 **Robust**: Extensive error handling, logging, and fallback mechanisms
- ⚡ **Fast**: Optimized performance with caching and async operations
- 📝 **Configurable**: YAML configuration for customization

---

## ✨ Features

### 🖥️ **System Tools** (7 tools)
- System Information (with neofetch integration)
- System Uptime
- Disk Usage (with visual bars)
- Memory Usage (RAM & SWAP)
- Running Processes (top 20 by memory)
- System Update (multi-distro support)
- System Clean (temp files & cache)

### 🌐 **Network Tools** (7 tools)
- Network Information
- Ping Host/IP
- Traceroute
- Port Scanner (common ports)
- Internet Speed Test
- DNS Lookup
- WHOIS Lookup

### 🔒 **Security Tools** (5 tools)
- Password Strength Checker
- Password Generator
- Hash Generator (MD5, SHA1, SHA256, SHA512)
- Malware Scanner (ClamAV, chkrootkit, rkhunter)
- File Encryption/Decryption

### 📍 **IP Tools** (3 tools)
- Geolocate IP
- My Public IP
- IP Calculator (subnet information)

### 📥 **Download Tools** (3 tools)
- YouTube Downloader (video/audio)
- File Downloader
- Batch Downloader

### 🛠️ **Utilities** (5 tools)
- Temporary Email
- QR Code Generator
- Text Encoder/Decoder (Base64, Hex, URL)
- JSON/YAML Formatter
- UUID Generator

### ⚙️ **Configuration** (4 tools)
- Update PyTools
- Settings
- View Logs
- About/Credits

---

## 🎉 What's New in v2.0.0

### Major Changes

#### **Complete Rewrite**
- Modular architecture with separated concerns
- Object-oriented design with base classes
- Proper Python package structure

#### **Enhanced UI**
- 3D ASCII art logo with gradient colors
- Category-based menu system
- Beautiful tables and panels using Rich library
- Progress bars with ETA
- Colored output with context-aware styling

#### **New Tools** (19 new tools added!)
- System Clean
- Port Scanner
- Speed Test
- DNS Lookup
- WHOIS Lookup
- Password Generator
- Hash Generator
- File Encryption
- My Public IP
- IP Calculator
- File Downloader
- Batch Downloader
- QR Code Generator
- Text Encoder/Decoder
- JSON/YAML Formatter
- UUID Generator
- Settings Manager
- Log Viewer
- About/Credits

#### **Improved Existing Tools**
- Better system detection (Windows, macOS, Linux, Termux)
- Multi-package manager support (apt, dnf, yum, pacman, brew, pkg)
- Enhanced error handling and fallbacks
- Progress tracking for long operations
- Caching for improved performance

#### **Configuration System**
- YAML-based configuration
- Persistent settings
- Customizable paths and preferences
- Theme support

#### **Better Logging**
- Rotating log files
- Configurable log levels
- Detailed error tracking

---

## 🔧 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- git

### System Dependencies (Optional)

**For full functionality, install these system tools:**

#### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install -y git python3 python3-pip neofetch figlet lolcat
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install -y git python3 python3-pip neofetch figlet
```

#### macOS
```bash
brew install git python3 neofetch figlet
```

#### Android (Termux)
```bash
pkg update
pkg install -y git python neofetch figlet
```

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/V4mpw0L/PyTools.git
cd PyTools
```

2. **Install Python dependencies**
```bash
# Install required dependencies
pip install -r requirements.txt

# Or install core dependencies only
pip install rich requests psutil pyyaml
```

3. **Run PyTools**
```bash
python3 pytools.py
```

### Optional Dependencies

For additional features, install these optional packages:

```bash
# YouTube downloads
pip install yt-dlp

# Network speed test
pip install speedtest-cli

# QR codes
pip install qrcode[pil]

# WHOIS lookup
pip install python-whois

# Progress bars
pip install tqdm
```

---

## 🚀 Usage

### Basic Usage

```bash
python3 pytools.py
```

### First Run

On first run, PyTools will:
1. Check Python version compatibility
2. Verify required dependencies
3. Create configuration directory
4. Generate default config.yaml
5. Show startup animation
6. Display main menu

### Navigation

- Use **number keys** to select options
- Press **Enter** to confirm
- Press **Ctrl+C** to go back or exit
- Follow on-screen prompts

### Example Workflow

1. **System Monitoring**
   - Select "1. 🖥️ System Tools"
   - Choose "1. System Information"
   - View comprehensive system details

2. **Network Diagnostics**
   - Select "2. 🌐 Network Tools"
   - Choose "2. Ping Host/IP"
   - Enter hostname or IP address
   - View ping results

3. **Download YouTube Video**
   - Select "5. 📥 Download Tools"
   - Choose "1. YouTube Downloader"
   - Paste YouTube URL
   - Select video or audio
   - Wait for download

---

## 📂 Tool Categories

### Category Overview

```
PyTools v2.0.0
├── 🖥️  System Tools        (7 modules)
├── 🌐 Network Tools       (7 modules)
├── 🔒 Security Tools      (5 modules)
├── 📍 IP Tools            (3 modules)
├── 📥 Download Tools      (3 modules)
├── 🛠️  Utilities          (5 modules)
└── ⚙️  Configuration      (4 modules)
```

### Detailed Tool List

<details>
<summary><b>🖥️ System Tools</b></summary>

1. **System Information** - Display detailed system information
2. **System Uptime** - Show system uptime
3. **Disk Usage** - Display disk space usage
4. **Memory Usage** - Show RAM and swap usage
5. **List Processes** - Display running processes
6. **Update System** - Update system packages
7. **Clean System** - Clean temporary files and caches

</details>

<details>
<summary><b>🌐 Network Tools</b></summary>

1. **Network Information** - Display network interfaces
2. **Ping Host/IP** - Test connectivity
3. **Traceroute** - Trace route to destination
4. **Port Scanner** - Scan common ports
5. **Speed Test** - Test internet speed
6. **DNS Lookup** - Resolve domain names
7. **WHOIS Lookup** - Get domain information

</details>

<details>
<summary><b>🔒 Security Tools</b></summary>

1. **Password Strength** - Check password strength
2. **Password Generator** - Generate secure passwords
3. **Hash Generator** - Generate file/text hashes
4. **Malware Scanner** - Scan for malware
5. **File Encryption** - Encrypt/decrypt files

</details>

<details>
<summary><b>📍 IP Tools</b></summary>

1. **Geolocate IP** - Get IP geolocation
2. **My Public IP** - Display your public IP
3. **IP Calculator** - Calculate subnet information

</details>

<details>
<summary><b>📥 Download Tools</b></summary>

1. **YouTube Downloader** - Download videos/audio
2. **File Downloader** - Download from URLs
3. **Batch Downloader** - Download multiple files

</details>

<details>
<summary><b>🛠️ Utilities</b></summary>

1. **Temporary Email** - Generate disposable emails
2. **QR Code Generator** - Create QR codes
3. **Text Encoder** - Encode/decode text
4. **JSON Formatter** - Format and validate JSON
5. **UUID Generator** - Generate UUIDs

</details>

---

## ⚙️ Configuration

### Configuration File

PyTools uses `~/.config/pytools/config.yaml` (Linux/macOS) or `%APPDATA%/PyTools/config.yaml` (Windows).

### Configuration Options

```yaml
# Theme
theme: "cyberpunk"

# Downloads
downloads:
  video_path: "VideosDownloads"
  audio_path: "AudiosDownloads"
  general_path: "Downloads"

# Network
network:
  timeout: 10
  ping_count: 4

# Security
security:
  min_password_length: 12

# Display
show_animations: true
```

### Editing Configuration

1. Run PyTools
2. Go to "⚙️ Configuration"
3. Select "Settings"
4. Edit configuration file directly or reset to defaults

---

## 📸 Screenshots


*![Image](https://github.com/user-attachments/assets/caecdb86-3dab-42e2-ab86-1a497d2bf4db)*


---

## 💻 Compatibility

### Operating Systems

| OS | Status | Notes |
|---|---|---|
| Linux (Debian/Ubuntu) | ✅ Full Support | Tested extensively |
| Linux (Fedora/RHEL) | ✅ Full Support | Multi-distro support |
| Linux (Arch) | ✅ Full Support | Pacman support |
| macOS | ✅ Full Support | Homebrew support |
| Windows | ⚠️ Partial Support | Some tools limited |
| Android (Termux) | ✅ Full Support | Optimized for mobile |

### Python Versions

- Python 3.7+ ✅
- Python 3.6 ❌
- Python 2.x ❌

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs** - Open an issue on GitHub
2. **Suggest Features** - Share your ideas
3. **Submit Pull Requests** - Fix bugs or add features
4. **Improve Documentation** - Help others understand PyTools
5. **Spread the Word** - Star the repo and share!

### Development Setup

```bash
git clone https://github.com/V4mpw0L/PyTools.git
cd PyTools
pip install -r requirements.txt
python3 pytools_v2.py
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

```
MIT License

Copyright (c) 2025 V4mpw0L

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 👏 Credits

### Creator

**V4mpw0L** (2025)

### Special Thanks

- Python community for amazing libraries
- Rich library by Will McGugan
- All contributors and users

### Libraries Used

- **rich** - Beautiful terminal formatting
- **requests** - HTTP library
- **psutil** - System utilities
- **pyyaml** - YAML support
- **yt-dlp** - YouTube downloads
- **speedtest-cli** - Speed testing
- **qrcode** - QR code generation
- And many more...

---

## 🔗 Links

- **GitHub**: https://github.com/V4mpw0L/PyTools
- **Issues**: https://github.com/V4mpw0L/PyTools/issues
- **Discussions**: https://github.com/V4mpw0L/PyTools/discussions

---

## 📊 Project Stats

- **Version**: 2.0.0
- **Release Date**: 2025
- **Total Lines of Code**: 5000+
- **Total Tools**: 34+
- **Categories**: 7
- **Supported Platforms**: 6

---

## 🎯 Roadmap

### Future Plans (v2.1.0+)

- [ ] Web interface (optional)
- [ ] Plugin system
- [ ] Multi-language support
- [ ] Cloud backup integration
- [ ] Scheduled tasks
- [ ] Remote system management
- [ ] Docker image
- [ ] Snap/Flatpak packages
- [ ] More security tools
- [ ] AI-powered suggestions

---

## ⭐ Star History

If you find PyTools useful, please consider giving it a star on GitHub! ⭐

---

<div align="center">

**Made with ❤️ and Python 🐍**

[⬆ Back to Top](#pytools-v200-)

</div>
