#!/bin/bash

# Load config
repo=$(uv run tomlq '.openwrt.repo' base-config.toml | tr -d '"')
tag=$(uv run tomlq '.openwrt.tag' base-config.toml | tr -d '"')

# Clone and checkout tag
git clone $repo openwrt
cd openwrt
git checkout $tag
