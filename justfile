# WayruOS build system using just
# https://github.com/casey/just

set shell := ["bash", "-c"]

# Default variables
openwrt_dir := "openwrt"
tools_dir := "tools"

# Show available recipes
default:
    @just --list

# Set up Python environment and install dependencies
setup:
    @echo "Setting up Python environment with uv..."
    uv sync

# Clone OpenWrt repository
clone-openwrt:
    uv run python {{tools_dir}}/clone-openwrt.py

# Update and install OpenWrt feeds
update-feeds:
    cd {{openwrt_dir}} && ./scripts/feeds update -a
    cd {{openwrt_dir}} && ./scripts/feeds install -a

# Uninstall OpenWrt feeds
uninstall-feeds:
    cd {{openwrt_dir}} && ./scripts/feeds uninstall -a

# Add device-specific patches
add-patches:
    uv run python {{tools_dir}}/add_patches.py

# Force re-apply device-specific patches
add-patches-force:
    uv run python {{tools_dir}}/add_patches.py --force

# Configure OpenWrt feeds
configure-feeds:
    uv run python {{tools_dir}}/configure-feeds.py

# Configure build system with wayru-os profiles
configure:
    uv run python {{tools_dir}}/configure.py

# Generate default configuration
defconfig:
    make -C {{openwrt_dir}} defconfig

# Build firmware (optimized)
build:
    make -C {{openwrt_dir}} -j$(nproc) download clean world

# Build firmware (debug mode)
build-debug:
    make -C {{openwrt_dir}} -j1 V=s

# Upload build artifacts
upload-build:
    uv run python {{tools_dir}}/upload-build.py

# Clean OpenWrt build directory
clean-openwrt:
    cd {{openwrt_dir}} && make clean

# Reset: remove OpenWrt directory
reset:
    rm -rf {{openwrt_dir}} || echo "OpenWrt directory not found, skipping..."

# Complete setup and build process
full-build: setup clone-openwrt add-patches configure-feeds update-feeds configure defconfig build

# Development workflow: configure and build
dev-build: add-patches configure-feeds update-feeds configure defconfig build

# Clean everything and start fresh
clean-all: reset
    @echo "Cleaned OpenWrt directory"

# Check Python environment and dependencies
check:
    @echo "Checking Python environment..."
    uv run python --version
    @echo "Checking dependencies..."
    uv pip list

# Run linting and formatting
lint:
    uv run python -m py_compile {{tools_dir}}/*.py

# Show build information
info:
    @echo "WayruOS Build System"
    @echo "==================="
    @echo "OpenWrt directory: {{openwrt_dir}}"
    @echo "Tools directory: {{tools_dir}}"
    @echo "Python environment:"
    @uv run python --version || echo "Python not available"
    @echo ""
    @echo "Available profiles:"
    @ls profiles/ 2>/dev/null || echo "No profiles directory found"
