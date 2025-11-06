# PyTools v2.0.0 - Quick Start Guide

Welcome to PyTools v2.0.0! This guide will help you get started in minutes.

---

## 📦 Quick Installation (3 Steps)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/V4mpw0L/PyTools.git
cd PyTools
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements_v2.txt
```

### 3️⃣ Run PyTools
```bash
python3 pytools_v2.py
```

---

## 🚀 Automated Installation (Recommended)

For automatic setup with system dependencies:

```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check Python version
- ✅ Detect your OS
- ✅ Install system dependencies (optional)
- ✅ Install Python packages
- ✅ Create configuration
- ✅ Set up command alias (optional)
- ✅ Launch PyTools

---

## 🎮 First Run

When you first run PyTools, you'll see:

1. **Dependency Check** - Verifies all required packages
2. **Startup Animation** - Beautiful 3D ASCII art
3. **Main Menu** - 7 category options

### Navigation
- Type a **number** and press **Enter** to select
- **Ctrl+C** to go back or exit
- Follow on-screen prompts

---

## 🔥 Quick Examples

### Example 1: Check System Info
```
1. Select "🖥️ System Tools"
2. Choose "1. System Information"
3. View comprehensive system details
```

### Example 2: Test Internet Speed
```
1. Select "🌐 Network Tools"
2. Choose "5. Internet Speed Test"
3. Wait for results
```

### Example 3: Download YouTube Video
```
1. Select "📥 Download Tools"
2. Choose "1. YouTube Downloader"
3. Paste YouTube URL
4. Select video or audio
5. Wait for download to complete
```

### Example 4: Generate Password
```
1. Select "🔒 Security Tools"
2. Choose "2. Password Generator"
3. Set password length
4. Choose special characters option
5. Copy your secure password
```

---

## 📋 Available Categories

| Icon | Category | Tools | Description |
|------|----------|-------|-------------|
| 🖥️ | System Tools | 7 | Monitoring & management |
| 🌐 | Network Tools | 7 | Diagnostics & testing |
| 🔒 | Security Tools | 5 | Analysis & protection |
| 📍 | IP Tools | 3 | IP utilities & geolocation |
| 📥 | Download Tools | 3 | YouTube & file downloads |
| 🛠️ | Utilities | 5 | QR codes, encoders, etc. |
| ⚙️ | Configuration | 4 | Settings & management |

**Total: 34+ Tools**

---

## ⚙️ Configuration

### Location
- **Linux/macOS**: `~/.config/pytools/config.yaml`
- **Windows**: `%APPDATA%\PyTools\config.yaml`
- **Termux**: `~/.config/pytools/config.yaml`

### Quick Settings
```yaml
theme: "cyberpunk"
show_animations: true

downloads:
  video_path: "VideosDownloads"
  audio_path: "AudiosDownloads"

network:
  timeout: 10
  ping_count: 4
```

Edit with your favorite text editor or use the built-in Settings Manager (⚙️ Configuration → Settings).

---

## 🔧 Troubleshooting

### Issue: Missing Dependencies
```bash
pip install rich requests psutil pyyaml
```

### Issue: YouTube Download Fails
```bash
pip install yt-dlp
```

### Issue: Speed Test Not Working
```bash
pip install speedtest-cli
```

### Issue: Permission Denied
```bash
chmod +x pytools_v2.py
```

### Issue: Module Not Found
```bash
# Make sure you're in the PyTools directory
cd PyTools
python3 pytools_v2.py
```

---

## 💡 Pro Tips

1. **Create Alias** - Add to `~/.bashrc` or `~/.zshrc`:
   ```bash
   alias pytools='python3 ~/PyTools/pytools_v2.py'
   ```

2. **Update PyTools** - Use built-in updater:
   ```
   ⚙️ Configuration → Update PyTools
   ```

3. **View Logs** - Check logs for errors:
   ```
   ⚙️ Configuration → View Logs
   ```

4. **Customize Downloads** - Change download paths in config.yaml

5. **Check Your IP** - Quick way to find your public IP:
   ```
   📍 IP Tools → My Public IP
   ```

---

## 📚 Next Steps

- **Read Full Documentation**: Check [README_v2.md](README_v2.md)
- **Review Changelog**: See [CHANGELOG.md](CHANGELOG.md)
- **Explore All Tools**: Try each category
- **Customize Settings**: Edit config.yaml
- **Star on GitHub**: https://github.com/V4mpw0L/PyTools

---

## 🆘 Need Help?

- **Documentation**: [README_v2.md](README_v2.md)
- **GitHub Issues**: https://github.com/V4mpw0L/PyTools/issues
- **Discussions**: https://github.com/V4mpw0L/PyTools/discussions

---

## 🎯 Most Popular Tools

Based on user feedback, these are the most used tools:

1. 📺 **YouTube Downloader** - Download videos and audio
2. 🖥️ **System Information** - Comprehensive system details
3. 🔐 **Password Generator** - Create secure passwords
4. ⚡ **Speed Test** - Test internet connection
5. 📧 **Temporary Email** - Disposable email addresses
6. 🌍 **Geolocate IP** - Find location of any IP
7. 🔍 **Port Scanner** - Scan open ports
8. 💾 **Disk Usage** - Check disk space
9. 🔒 **Password Checker** - Analyze password strength
10. 📱 **QR Code Generator** - Create QR codes

---

## ⚡ Keyboard Shortcuts

- **Ctrl+C** - Cancel operation / Go back
- **Enter** - Confirm selection
- **Arrow Keys** - Navigation (in some prompts)

---

## 🌟 Quick Commands

If you created an alias:

```bash
pytools              # Launch PyTools
```

Without alias:
```bash
cd ~/PyTools
python3 pytools_v2.py
```

---

## 📊 System Requirements

- **Python**: 3.7 or higher
- **RAM**: 256MB minimum
- **Disk**: 100MB free space
- **OS**: Linux, macOS, Windows, Termux
- **Internet**: Required for most features

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] PyTools launches without errors
- [ ] Main menu displays correctly
- [ ] At least one tool runs successfully
- [ ] Configuration file created
- [ ] Logs are being written

If all checked, you're ready to go! 🎉

---

## 🚀 Ready to Explore?

Launch PyTools now:
```bash
python3 pytools_v2.py
```

Have fun exploring all 34+ tools! 💪

---

**Made with ❤️ by V4mpw0L | License: MIT**