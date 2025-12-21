#!/usr/bin/env bash

# Exit on error
set -e

echo "=== Beads Installation Script ==="
echo ""
echo "Beads is a distributed, git-backed issue tracking system for AI coding agents."
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect operating system
OS="$(uname -s)"
case "$OS" in
    Linux*)     PLATFORM="Linux";;
    Darwin*)    PLATFORM="macOS";;
    MINGW*|MSYS*|CYGWIN*) PLATFORM="Windows";;
    *)          PLATFORM="Unknown";;
esac

echo "Detected platform: $PLATFORM"
echo ""

# Try to install Beads using available package managers
INSTALLED=false

# Method 1: Try Homebrew (macOS/Linux)
if command_exists brew; then
    echo "📦 Found Homebrew, installing Beads..."
    brew install steveyegge/beads/bd
    INSTALLED=true
    INSTALL_METHOD="Homebrew"

# Method 2: Try npm
elif command_exists npm; then
    echo "📦 Found npm, installing Beads globally..."
    npm install -g @beads/bd
    INSTALLED=true
    INSTALL_METHOD="npm"

# Method 3: Try Go
elif command_exists go; then
    echo "📦 Found Go, installing Beads..."
    go install github.com/steveyegge/beads/cmd/bd@latest
    INSTALLED=true
    INSTALL_METHOD="Go"

# Method 4: Use installation script (Linux/macOS only)
elif [ "$PLATFORM" != "Windows" ]; then
    echo "📦 No package manager found, using installation script..."
    curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
    INSTALLED=true
    INSTALL_METHOD="installation script"

else
    echo "❌ Error: No compatible package manager found (npm, brew, or go)"
    echo ""
    echo "Please install one of the following:"
    echo "  - Node.js and npm: https://nodejs.org/"
    echo "  - Homebrew: https://brew.sh/"
    echo "  - Go: https://go.dev/"
    echo ""
    echo "Or install manually from: https://github.com/steveyegge/beads"
    exit 1
fi

if [ "$INSTALLED" = true ]; then
    echo ""
    echo "✅ Beads installed successfully via $INSTALL_METHOD"
    echo ""

    # Verify installation
    if command_exists bd; then
        echo "🔍 Verifying installation..."
        bd --version || echo "Beads command 'bd' is available"
        echo ""

        # Initialize Beads in stealth mode
        echo "🚀 Initializing Beads in stealth mode for this project..."
        echo "   (Stealth mode keeps .beads/ in .gitignore for local use only)"
        echo ""

        if bd init --stealth; then
            echo ""
            echo "✅ Beads initialized successfully in stealth mode!"
        else
            echo ""
            echo "ℹ️  Beads may already be initialized. Run 'bd --help' for usage."
        fi

        echo ""
        echo "📚 Quick start commands:"
        echo "  bd ready              - View tasks without blockers"
        echo "  bd create \"Title\"     - Create a new task"
        echo "  bd show <id>          - Show task details"
        echo "  bd quickstart         - Interactive guide for AI agents"
        echo "  bd --help             - Show all commands"
        echo ""
        echo "📖 Learn more: https://github.com/steveyegge/beads"
    else
        echo "⚠️  Installation completed but 'bd' command not found in PATH"
        echo "   You may need to restart your shell or add it to your PATH manually"
    fi
fi

echo ""
echo "Done! 🎉"
