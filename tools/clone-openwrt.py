#!/usr/bin/env python3

import os
import sys
import subprocess
import toml
import time
import threading
from tqdm import tqdm


def monitor_clone_progress(process, target_dir):
    """Monitor git clone progress by checking directory size"""
    with tqdm(desc="Cloning", unit="B", unit_scale=True, colour="green") as pbar:
        last_size = 0
        while process.poll() is None:
            if os.path.exists(target_dir):
                try:
                    # Get directory size
                    result = subprocess.run(
                        ["du", "-sb", target_dir],
                        capture_output=True,
                        text=True,
                        timeout=1
                    )
                    if result.returncode == 0:
                        current_size = int(result.stdout.split()[0])
                        if current_size > last_size:
                            pbar.update(current_size - last_size)
                            last_size = current_size
                except (subprocess.TimeoutExpired, ValueError, IndexError):
                    pass
            time.sleep(0.5)

        # Final update
        if os.path.exists(target_dir):
            try:
                result = subprocess.run(
                    ["du", "-sb", target_dir],
                    capture_output=True,
                    text=True,
                    timeout=1
                )
                if result.returncode == 0:
                    final_size = int(result.stdout.split()[0])
                    pbar.update(final_size - last_size)
            except (subprocess.TimeoutExpired, ValueError, IndexError):
                pass


def main():
    # Check if openwrt folder already exists
    if os.path.exists("openwrt"):
        print("Error: openwrt folder already exists. Please remove it first or use a different location.")
        sys.exit(1)

    # Load config
    print("Loading configuration...")
    try:
        config = toml.load("base-config.toml")
        repo = config["openwrt"]["repo"]
        tag = config["openwrt"]["tag"]
    except (FileNotFoundError, KeyError) as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

    print(f"Repository: {repo}")
    print(f"Tag: {tag}")

    # Clone with progress monitoring
    print(f"Cloning OpenWrt repository (tag: {tag})...")
    try:
        process = subprocess.Popen(
            ["git", "clone", "--branch", tag, repo, "openwrt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Monitor progress in a separate thread
        progress_thread = threading.Thread(
            target=monitor_clone_progress,
            args=(process, "openwrt")
        )
        progress_thread.start()

        # Wait for clone to complete
        process.wait()
        progress_thread.join()

        if process.returncode != 0:
            print("Error: Git clone failed")
            sys.exit(1)

    except Exception as e:
        print(f"Error during clone: {e}")
        sys.exit(1)

    print(f"Successfully cloned tag {tag}")

    print("OpenWrt clone completed successfully!")


if __name__ == "__main__":
    main()
