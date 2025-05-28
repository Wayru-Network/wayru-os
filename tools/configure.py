import toml
import json
from dotenv import load_dotenv
import os
import shutil

TMP_PATH = 'tmp'
DIFFCONFIG_FILE = 'diffconfig'
DEVICE_JSON_FILE = 'device.json'
BANNER_FILE = 'banner'

def generate_build_config(base_config, firmware_config):
    os_name = base_config["general"]["os_name"]
    os_version = base_config["general"]["os_version"]

    target = firmware_config["build"]["target"]
    subtarget = firmware_config["build"]["subtarget"]
    profile = firmware_config["build"]["device_profile"]

    diffconfig_path = os.path.join(TMP_PATH, DIFFCONFIG_FILE)
    with open(diffconfig_path, 'w') as build_config_file:
        build_config_file.write(f'CONFIG_TARGET_{target}=y\n')
        build_config_file.write(f'CONFIG_TARGET_{target}_{subtarget}=y\n')
        build_config_file.write(f'CONFIG_TARGET_{target}_{subtarget}_DEVICE_{profile}=y\n')
        build_config_file.write(f'CONFIG_IMAGEOPT=y\n')
        build_config_file.write(f'CONFIG_VERSIONOPT=y\n')
        build_config_file.write(f'CONFIG_VERSION_BUG_URL=""\n')
        build_config_file.write(f'CONFIG_VERSION_CODE=""\n')
        build_config_file.write(f'CONFIG_VERSION_CODE_FILENAMES=y\n')
        build_config_file.write(f'CONFIG_VERSION_DIST="{os_name}"\n')
        build_config_file.write(f'CONFIG_VERSION_FILENAMES=y\n')
        build_config_file.write(f'CONFIG_VERSION_HOME_URL=""\n')
        build_config_file.write(f'CONFIG_VERSION_HWREV=""\n')
        build_config_file.write(f'CONFIG_VERSION_MANUFACTURER=""\n')
        build_config_file.write(f'CONFIG_VERSION_MANUFACTURER_URL=""\n')
        build_config_file.write(f'CONFIG_VERSION_NUMBER="{os_version}"\n')
        build_config_file.write(f'CONFIG_VERSION_PRODUCT=""\n')
        build_config_file.write(f'CONFIG_VERSION_REPO=""\n')
        build_config_file.write(f'CONFIG_VERSION_SUPPORT_URL=""\n')

        base_packages = firmware_config["packages"]["base"]
        for package in base_packages:
            if package == "dnsmasq-full":
                build_config_file.write('# CONFIG_PACKAGE_dnsmasq is not set\n')

            build_config_file.write(f'CONFIG_PACKAGE_{package}=y\n')

def generate_device_json(codename: str, brand: str, model: str) -> None:
    data = {
        "name": codename,
        "brand": brand,
        "model": model,
    }

    device_json_path = os.path.join(TMP_PATH, DEVICE_JSON_FILE)
    with open(device_json_path, 'w') as device_json_file:
        json.dump(data, device_json_file, indent=2)

def generate_banner(codename: str, version: str) -> None:
    # Read the ASCII logo file at resources/ascii-logo and load it into a variable
    ascii_logo = ''
    with open('resources/ascii-logo', 'r') as ascii_logo_file:
        ascii_logo = ascii_logo_file.read()

    # Prepare the rest of the banner
    separator = '---------------------------------------------'
    variant_codename = f'variant codename: {codename}'
    version = f'version: {version}'

    # Build the banner with the ascii logo, the separator and the details
    banner = f'{ascii_logo}\n{separator}\n{variant_codename}\n{version}\n{separator}\n'

    banner_path = os.path.join(TMP_PATH, BANNER_FILE)
    with open(banner_path, 'w') as banner_file:
        banner_file.write(banner)

def main():
    # Load env
    load_dotenv()
    selected_profile = os.getenv('PROFILE')

    # Prep tmp directory
    os.makedirs(TMP_PATH, exist_ok=True)

    # Load base config
    base_config_path = 'base-config.toml'
    base_config = toml.load(base_config_path)

    # Load profile config
    profile_config_path = f'profiles/{selected_profile}/profile-config.toml'
    profile_config = toml.load(profile_config_path)

    # Generate build config
    generate_build_config(base_config, profile_config)

    # Generate device JSON file
    codename = profile_config["general"]["codename"]
    brand = profile_config["general"]["brand"]
    model = profile_config["general"]["model"]
    generate_device_json(codename, brand, model)

    # Generate banner
    generate_banner(codename, base_config["general"]["os_version"])

    # @todo Fetch shadow file from secrets vault

    os_name = base_config['general']['os_name']

    # Create needed directories to ship files with the build
    os_name = base_config['general']['os_name']
    os.makedirs('openwrt/files/etc/uci-defaults', exist_ok=True)
    os.makedirs('openwrt/files/etc/config', exist_ok=True)
    os.makedirs(f'openwrt/files/etc/{os_name}', exist_ok=True)

    # Copy uci-defaults
    shutil.copytree(f'profiles/{selected_profile}/uci-defaults', 'openwrt/files/etc/uci-defaults', dirs_exist_ok=True)

    # Copy config (if exists)
    if os.path.exists(f'profiles/{selected_profile}/config'):
        shutil.copytree(f'profiles/{selected_profile}/config', 'openwrt/files/etc/config', dirs_exist_ok=True)

    # Copy device.json
    shutil.copy2(os.path.join(TMP_PATH, DEVICE_JSON_FILE), f'openwrt/files/etc/{os_name}/device.json')

    # Copy banner
    shutil.copy2(os.path.join(TMP_PATH, BANNER_FILE), f'openwrt/files/etc/banner')

    # Copy diffconfig
    shutil.copy2(os.path.join(TMP_PATH, DIFFCONFIG_FILE), 'openwrt/.config')

if __name__ == '__main__':
    main()
