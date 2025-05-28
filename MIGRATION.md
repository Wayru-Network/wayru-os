# Migration Guide: Makefile to Just + Requirements.txt to UV

This guide helps you migrate from the old build system to the new modernized tooling.

## Overview of Changes

### Before (Old System)
- **Make**: Used `Makefile` for task automation
- **pip**: Used `requirements.txt` for Python dependencies
- **Manual venv**: Required manual virtual environment setup

### After (New System)
- **Just**: Modern command runner with better syntax and features
- **UV**: Fast Python package installer and dependency management
- **Automated setup**: Single command environment setup

## Migration Steps

### 1. Install New Tools

#### Install Just
```bash
# Using Cargo (recommended)
cargo install just

# Using package managers
# macOS
brew install just

# Ubuntu/Debian
wget -qO - 'https://proget.makedeb.org/debian-feeds/prebuilt-mpr.pub' | gpg --dearmor | sudo tee /usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg 1> /dev/null
echo "deb [arch=all,amd64,arm64,armhf signed-by=/usr/share/keyrings/prebuilt-mpr-archive-keyring.gpg] https://proget.makedeb.org prebuilt-mpr $(lsb_release -cs)" | sudo tee /etc/apt/sources.list.d/prebuilt-mpr.list
sudo apt update
sudo apt install just

# Arch Linux
sudo pacman -S just
```

#### Install UV
```bash
# Using the official installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Using pip
pip install uv

# Using package managers
# macOS
brew install uv

# Windows
winget install --id=astral-sh.uv  -e
```

### 2. Command Translation

| Old Makefile Command | New Just Command | Notes |
|---------------------|------------------|-------|
| `make clone-openwrt` | `just clone-openwrt` | Identical functionality |
| `make update-feeds` | `just update-feeds` | Identical functionality |
| `make uninstall-feeds` | `just uninstall-feeds` | Identical functionality |
| `make add-patches` | `just add-patches` | Now uses `uv run` |
| `make configure` | `just configure` | Now uses `uv run` |
| `make defconfig` | `just defconfig` | Identical functionality |
| `make build` | `just build` | Identical functionality |
| `make build-debug` | `just build-debug` | Identical functionality |
| `make upload-build` | `just upload-build` | Now uses `uv run` |
| `make clean-openwrt` | `just clean-openwrt` | Identical functionality |
| `make reset` | `just reset` | Identical functionality |
| N/A | `just setup` | **NEW**: Sets up Python environment |
| N/A | `just full-build` | **NEW**: Complete build process |
| N/A | `just dev-build` | **NEW**: Development workflow |
| N/A | `just check` | **NEW**: Environment verification |
| N/A | `just info` | **NEW**: Build system information |

### 3. Environment Setup Changes

#### Old Method
```bash
# Manual virtual environment setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### New Method
```bash
# Single command setup
just setup
```

### 4. Development Workflow Changes

#### Old Workflow
```bash
# Initial setup
make clone-openwrt
make add-patches
make update-feeds
make configure
make defconfig
make build
make upload-build
```

#### New Workflow
```bash
# Initial setup
just full-build

# Development iterations
just dev-build
just upload-build
```

### 5. File Changes

#### Removed Files
- `requirements.txt` (replaced by `pyproject.toml`)
- `Makefile` (replaced by `justfile`)

#### New Files
- `pyproject.toml` - Python project configuration and dependencies
- `justfile` - Task runner configuration
- `MIGRATION.md` - This migration guide

#### Modified Files
- `README.md` - Updated documentation
- `pyrightconfig.json` - Updated for uv virtual environment path

### 6. Benefits of Migration

#### Performance
- **UV**: 10-100x faster than pip for dependency resolution and installation
- **Just**: Faster startup and better dependency handling than Make

#### Developer Experience
- **Better syntax**: Just uses a more readable syntax than Makefiles
- **Built-in help**: `just` command shows all available recipes
- **Better error messages**: More informative error reporting
- **Cross-platform**: Better Windows support

#### Dependency Management
- **Lock file**: UV generates `uv.lock` for reproducible builds
- **Unified config**: Single `pyproject.toml` file for all Python configuration
- **Automatic virtual environment**: UV handles virtual environments automatically

### 7. Troubleshooting

#### Just not found
```bash
# Make sure just is in your PATH
which just

# If using Cargo, make sure ~/.cargo/bin is in your PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### UV not found
```bash
# Make sure uv is in your PATH
which uv

# If using the installer, restart your shell or run:
source ~/.bashrc  # or ~/.zshrc
```

#### Python environment issues
```bash
# Reset the environment
rm -rf .venv
just setup
```

#### Old Make commands still being used
- Update any CI/CD scripts to use `just` instead of `make`
- Update documentation and team processes
- Consider adding a deprecated `Makefile` that forwards to just commands during transition

### 8. Backwards Compatibility

During the transition period, you can create a simple `Makefile` that forwards commands to just:

```makefile
# Backwards compatibility Makefile
%:
	@echo "WARNING: Makefile is deprecated. Please use 'just $@' instead."
	@just $@
```

This allows old commands to work while encouraging migration to the new system.