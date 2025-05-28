# Backwards compatibility Makefile
# This Makefile forwards commands to the new just-based build system
# Please migrate to using 'just' directly: https://github.com/casey/just

SHELL := /bin/bash

.PHONY: help clone-openwrt configure update-feeds uninstall-feeds add-patches defconfig build upload-build clean-openwrt reset build-debug setup full-build dev-build check info

# Default target shows deprecation warning and available commands
help:
	@echo "WARNING: This Makefile is deprecated and will be removed in a future version."
	@echo "Please migrate to using 'just' instead of 'make'"
	@echo ""
	@echo "Migration steps:"
	@echo "1. Install just: cargo install just"
	@echo "2. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
	@echo "3. Run the migration script: ./migrate.sh"
	@echo ""
	@echo "Available commands (use 'just <command>' instead):"
	@just --list 2>/dev/null || echo "ERROR: just is not installed. Please install it first."

# Forward all old commands to just with deprecation warning
clone-openwrt:
	@echo "WARNING: 'make clone-openwrt' is deprecated. Use 'just clone-openwrt' instead."
	@just clone-openwrt

configure:
	@echo "WARNING: 'make configure' is deprecated. Use 'just configure' instead."
	@just configure

update-feeds:
	@echo "WARNING: 'make update-feeds' is deprecated. Use 'just update-feeds' instead."
	@just update-feeds

uninstall-feeds:
	@echo "WARNING: 'make uninstall-feeds' is deprecated. Use 'just uninstall-feeds' instead."
	@just uninstall-feeds

add-patches:
	@echo "WARNING: 'make add-patches' is deprecated. Use 'just add-patches' instead."
	@just add-patches

defconfig:
	@echo "WARNING: 'make defconfig' is deprecated. Use 'just defconfig' instead."
	@just defconfig

build:
	@echo "WARNING: 'make build' is deprecated. Use 'just build' instead."
	@just build

build-debug:
	@echo "WARNING: 'make build-debug' is deprecated. Use 'just build-debug' instead."
	@just build-debug

upload-build:
	@echo "WARNING: 'make upload-build' is deprecated. Use 'just upload-build' instead."
	@just upload-build

clean-openwrt:
	@echo "WARNING: 'make clean-openwrt' is deprecated. Use 'just clean-openwrt' instead."
	@just clean-openwrt

reset:
	@echo "WARNING: 'make reset' is deprecated. Use 'just reset' instead."
	@just reset

# New commands that don't have make equivalents
setup:
	@echo "WARNING: 'make setup' is deprecated. Use 'just setup' instead."
	@just setup

full-build:
	@echo "WARNING: 'make full-build' is deprecated. Use 'just full-build' instead."
	@just full-build

dev-build:
	@echo "WARNING: 'make dev-build' is deprecated. Use 'just dev-build' instead."
	@just dev-build

check:
	@echo "WARNING: 'make check' is deprecated. Use 'just check' instead."
	@just check

info:
	@echo "WARNING: 'make info' is deprecated. Use 'just info' instead."
	@just info

# Catch-all for any other commands
%:
	@echo "WARNING: 'make $@' is deprecated. Use 'just $@' instead."
	@if just --list | grep -q "^[[:space:]]*$@[[:space:]]"; then \
		just $@; \
	else \
		echo "ERROR: Command '$@' not found in justfile"; \
		echo "Run 'just' to see available commands"; \
		exit 1; \
	fi