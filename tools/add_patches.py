import os
import subprocess
import sys
from dotenv import load_dotenv
import argparse

load_dotenv()

PROFILE_NAME = os.getenv('PROFILE')
PROFILE_DIR = os.path.join("profiles", PROFILE_NAME)
PATCH_DIR = os.path.join(PROFILE_DIR, "patches")
OPENWRT_DIR = os.path.join("openwrt")

def is_patch_applied(patch_file):
    """Check if a patch is already applied using patch --dry-run"""
    try:
        with open(patch_file, 'r') as patch:
            result = subprocess.run(
                ['patch', '-p1', '--dry-run', '--reverse'],
                stdin=patch,
                cwd=OPENWRT_DIR,
                capture_output=True,
                text=True
            )
            # If reverse patch succeeds, the patch is already applied
            return result.returncode == 0
    except Exception:
        return False

def apply_patch(patch_file, force=False):
    # Check if patch is already applied
    if not force and is_patch_applied(patch_file):
        print(f"Patch {patch_file} is already applied, skipping...")
        return True
    
    try:
        with open(patch_file, 'r') as patch:
            print(f"Applying patch: {patch_file}")
            
            # If forcing and patch is applied, reverse it first
            if force and is_patch_applied(patch_file):
                print(f"Force mode: reversing existing patch {patch_file}")
                with open(patch_file, 'r') as reverse_patch:
                    subprocess.run(
                        ['patch', '-p1', '--reverse'],
                        stdin=reverse_patch,
                        cwd=OPENWRT_DIR,
                        check=True,
                        text=True
                    )
            
            # Apply the patch
            with open(patch_file, 'r') as apply_patch:
                result = subprocess.run(
                    ['patch', '-p1'],
                    stdin=apply_patch,
                    cwd=OPENWRT_DIR,
                    check=True,
                    text=True
                )
                
            if result.returncode == 0:
                print(f"Patch {patch_file} applied correctly")
                return True
                
    except subprocess.CalledProcessError as e:
        print(f"Error applying patch: {patch_file}")
        print(f"Error details: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Apply patches to OpenWrt')
    parser.add_argument('--force', action='store_true', 
                       help='Force re-application of patches (reverse and re-apply)')
    args = parser.parse_args()
    
    # Check if the profile folder exists
    if not os.path.exists(PROFILE_DIR):
        print(f"Profile directory not found: {PROFILE_DIR}")
        sys.exit(1)
    
    # Check if the patches subfolder exists
    if not os.path.exists(PATCH_DIR):
        print(f"Patch folder not found in profile: {PATCH_DIR}. this profile does not need them.")
        sys.exit(0)

    patch_files = [f for f in os.listdir(PATCH_DIR) if f.endswith('.patch')]

    if not patch_files:
        print(f"No patches were found in {PATCH_DIR}")
        sys.exit(0)

    # Apply patches
    success = True
    for patch in patch_files:
        patch_file = os.path.join(PATCH_DIR, patch)
        if not apply_patch(patch_file, force=args.force):
            success = False
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()