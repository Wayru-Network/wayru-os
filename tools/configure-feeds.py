import toml
from dotenv import load_dotenv
import os

def main():
    # Load env
    load_dotenv()
    
    # Load base config
    base_config_path = 'base-config.toml'
    base_config = toml.load(base_config_path)

    # Set up feeds
    default_feeds_content = ''
    with open('openwrt/feeds.conf.default', 'r') as default_feeds_file:
        default_feeds_content = default_feeds_file.read()

    feeds = base_config['openwrt']['feeds']
    feeds_content = ''
    for feed in feeds:
        feeds_content += f'{feed["method"]} {feed["name"]} {feed["url"]}\n'

    with open('openwrt/feeds.conf', 'w') as feeds_file:
        feeds_file.write(feeds_content)
        feeds_file.write('\n')
        feeds_file.write(default_feeds_content)

if __name__ == '__main__':
    main()