#!/bin/bash
# PyTools v2.0.0 - Installation Script
# Author: V4mpw0L
# Description: Automated installation script for PyTools

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
show_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
    ██████╗ ██╗   ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝        ██║   ██║   ██║██║   ██║██║     ███████╗
    ██╔═══╝   ╚██╔╝         ██║   ██║   ██║██║   ██║██║     ╚════██║
    ██║        ██║          ██║   ╚██████╔╝╚██████╔╝███████╗███████║
    ╚═╝        ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
EOF
    echo -e "${NC}"
    echo -e "${GREEN}PyTools v2.0.0 - Installation Script${NC}"
    echo -e "${BLUE}Author: V4mpw0L | License: MIT${NC}"
    echo ""
}

# Print functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
            OS_VERSION=$VERSION_ID
        else
            OS="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi

    # Check for Termux
    if [ -n "$PREFIX" ] && [[ "$PREFIX" == *"com.termux"* ]]; then
        OS="termux"
    fi

    print_info "Detected OS: $OS"
}

# Check Python version
check_python() {
    print_info "Checking Python installation..."

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python not found. Please install Python 3.7 or higher."
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_error "Python 3.7+ required. Found: $PYTHON_VERSION"
        exit 1
    fi

    print_success "Python $PYTHON_VERSION found"
}

# Check pip
check_pip() {
    print_info "Checking pip installation..."

    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip not found. Installing pip..."

        if [ "$OS" = "termux" ]; then
            pkg install -y python-pip
        elif [ "$OS" = "macos" ]; then
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            $PYTHON_CMD get-pip.py
            rm get-pip.py
        else
            $PYTHON_CMD -m ensurepip --default-pip
        fi
    fi

    print_success "pip found"
}

# Install system dependencies
install_system_deps() {
    print_info "Installing system dependencies..."

    case "$OS" in
        ubuntu|debian|linuxmint)
            print_info "Using apt package manager..."
            sudo apt update
            sudo apt install -y git neofetch figlet 2>/dev/null || print_warning "Some optional packages failed to install"
            print_success "System dependencies installed"
            ;;
        fedora|rhel|centos)
            print_info "Using dnf/yum package manager..."
            if command -v dnf &> /dev/null; then
                sudo dnf install -y git neofetch figlet 2>/dev/null || print_warning "Some optional packages failed to install"
            else
                sudo yum install -y git neofetch figlet 2>/dev/null || print_warning "Some optional packages failed to install"
            fi
            print_success "System dependencies installed"
            ;;
        arch|manjaro)
            print_info "Using pacman package manager..."
            sudo pacman -Sy --noconfirm git neofetch figlet 2>/dev/null || print_warning "Some optional packages failed to install"
            print_success "System dependencies installed"
            ;;
        macos)
            print_info "Using Homebrew..."
            if ! command -v brew &> /dev/null; then
                print_warning "Homebrew not found. Install from https://brew.sh"
            else
                brew install git neofetch figlet 2>/dev/null || print_warning "Some optional packages failed to install"
                print_success "System dependencies installed"
            fi
            ;;
        termux)
            print_info "Using Termux pkg manager..."
            pkg update
            pkg install -y git neofetch figlet python 2>/dev/null || print_warning "Some optional packages failed to install"
            print_success "System dependencies installed"
            ;;
        *)
            print_warning "Unknown OS. Skipping system dependencies."
            ;;
    esac
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."

    # Core dependencies
    print_info "Installing core dependencies..."
    $PIP_CMD install rich requests psutil pyyaml --user --upgrade

    if [ $? -eq 0 ]; then
        print_success "Core dependencies installed"
    else
        print_error "Failed to install core dependencies"
        exit 1
    fi

    # Optional dependencies
    read -p "$(echo -e ${YELLOW}Install optional dependencies? \(recommended\) [Y/n]: ${NC})" install_optional
    install_optional=${install_optional:-Y}

    if [[ $install_optional =~ ^[Yy]$ ]]; then
        print_info "Installing optional dependencies..."
        $PIP_CMD install yt-dlp speedtest-cli qrcode[pil] python-whois tqdm --user --upgrade 2>/dev/null || print_warning "Some optional dependencies failed to install"
        print_success "Optional dependencies installation completed"
    fi
}

# Create config directory
create_config() {
    print_info "Creating configuration directory..."

    if [ "$OS" = "macos" ] || [ "$OS" = "linux-gnu" ] || [ "$OS" = "termux" ]; then
        CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/pytools"
    else
        CONFIG_DIR="$HOME/.pytools"
    fi

    mkdir -p "$CONFIG_DIR"

    if [ -f "config/config.yaml" ]; then
        if [ ! -f "$CONFIG_DIR/config.yaml" ]; then
            cp config/config.yaml "$CONFIG_DIR/config.yaml"
            print_success "Configuration file created at $CONFIG_DIR/config.yaml"
        else
            print_info "Configuration file already exists"
        fi
    fi
}

# Create alias
create_alias() {
    read -p "$(echo -e ${YELLOW}Create 'pytools' command alias? [Y/n]: ${NC})" create_alias
    create_alias=${create_alias:-Y}

    if [[ $create_alias =~ ^[Yy]$ ]]; then
        PYTOOLS_PATH="$(pwd)/pytools.py"

        # Detect shell
        SHELL_NAME=$(basename "$SHELL")

        case "$SHELL_NAME" in
            bash)
                SHELL_RC="$HOME/.bashrc"
                ;;
            zsh)
                SHELL_RC="$HOME/.zshrc"
                ;;
            fish)
                SHELL_RC="$HOME/.config/fish/config.fish"
                ;;
            *)
                SHELL_RC="$HOME/.profile"
                ;;
        esac

        # Add alias
        ALIAS_CMD="alias pytools='$PYTHON_CMD $PYTOOLS_PATH'"

        if ! grep -q "alias pytools=" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# PyTools alias" >> "$SHELL_RC"
            echo "$ALIAS_CMD" >> "$SHELL_RC"
            print_success "Alias added to $SHELL_RC"
            print_info "Run 'source $SHELL_RC' or restart your terminal"
        else
            print_info "Alias already exists in $SHELL_RC"
        fi
    fi
}

# Run PyTools
run_pytools() {
    read -p "$(echo -e ${GREEN}Run PyTools now? [Y/n]: ${NC})" run_now
    run_now=${run_now:-Y}

    if [[ $run_now =~ ^[Yy]$ ]]; then
        echo ""
        print_info "Starting PyTools..."
        sleep 1
        $PYTHON_CMD pytools.py
    fi
}

# Main installation
main() {
    show_banner

    print_info "Starting PyTools v2.0.0 installation..."
    echo ""

    # Detect OS
    detect_os
    echo ""

    # Check Python
    check_python
    echo ""

    # Check pip
    check_pip
    echo ""

    # Install system dependencies
    read -p "$(echo -e ${YELLOW}Install system dependencies? [Y/n]: ${NC})" install_sys
    install_sys=${install_sys:-Y}

    if [[ $install_sys =~ ^[Yy]$ ]]; then
        install_system_deps
        echo ""
    fi

    # Install Python dependencies
    install_python_deps
    echo ""

    # Create config
    create_config
    echo ""

    # Create alias
    create_alias
    echo ""

    # Installation complete
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                        ║${NC}"
    echo -e "${GREEN}║  ✓ Installation completed successfully ║${NC}"
    echo -e "${GREEN}║                                        ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""

    print_info "PyTools v2.0.0 is ready to use!"
    print_info "Run: python3 pytools.py"
    echo ""

    # Run PyTools
    run_pytools
}

# Run main
main
