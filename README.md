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
Make sure to have installed:
- `make`
- `git`
- `tomlq`
- `python3` aliased as `python` (highly recommend using a virtual environment)
- python dependencies: `pip install -r requirements.txt`
- Dependencies needed to build OpenWrt: https://openwrt.org/docs/guide-developer/toolchain/install-buildsystem

## Repo tools
- Clone the OpenWrt repository `make clone-openwrt`
- Configure build system with wayru-os profiels `make configure`
  - Make sure to have specified the profile in the `.env` file
- Complete the configuration with the OpenWrt build system `make menuconfig`
- Build the firmware `make build`
- Upload builds `make upload`

## Upload builds
TBD
