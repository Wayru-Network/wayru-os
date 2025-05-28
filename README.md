# wayru-os
```
 _       __                       ____  _____
| |     / /___ ___  _________  __/ __ \/ ___/
| | /| / / __ `/ / / / ___/ / / / / / /\__ \
| |/ |/ / /_/ / /_/ / /  / /_/ / /_/ /___/ /
|__/|__/\__,_/\__, /_/   \__,_/\____//____/
             /____/
```
WayruOS is a Linux distribution based on OpenWrt. It is designed to be used in routers and other embedded devices. It runs Wayru's operator services and applications.

This repository contains the configuration files to build WayruOS with the OpenWrt build system. It also contains device profiles that include configuration and dependencies specific to each device.

## Features

- Enterprise networks and Passpoint
- Captive portal
- OpenWISP integration
- OpenVPN integration
- Wayru onboarding
- Wayru monitoring
- Wayru firmware upgrades

## Supported devices

Check the profiles directory for the supported devices.

## Configuration

This repository contains configuration files to build WayruOS.
- Base firmware configuration: `base-config.toml`
- Per-device configuration: `profiles/<device-codename>/profile-config.toml`

## Versioning

WayruOS uses [Semantic Versioning](https://semver.org/).

The firmware version is composed of 4 parts:
- Device codename
- Major version: typically follows the OpenWrt version (e.g. 21, 22, 23)
- Minor version: incremented for each release with new features
- Patch version: incremented for each build that includes bug fixes or small improvements

Format: `wayru-os-{device-codename}-{major}.{minor}.{patch}`

Example: `wayru-os-genesis-23.1.0`

## Repo setup
Make sure to install:
- `just`
- `uv`
- `git`
- Dependencies needed to build OpenWrt: https://openwrt.org/docs/guide-developer/toolchain/install-buildsystem

### Quick setup:
1. Install `just`: `cargo install just` or use your package manager
2. Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh` or `pip install uv`
3. Set up the Python environment: `just setup`

## Repo tools
The repo has tools to configure, build, and publish wayru-os images.

Check the `justfile` and the `tools` folder for a better understanding of the tools available.

You can also run `just` to show all available recipes.

### Quick start:
To set up and build a wayru-os image, you can follow these steps:
1. Set up the environment: `just setup`
2. Configure your profile in the `.env` file (copy from `.env.example`)
3. Run the complete build: `just full-build`

### Development workflow:
For iterative development after initial setup:
- Make changes to configuration
- Run: `just dev-build`
- Upload when ready: `just upload-build`
