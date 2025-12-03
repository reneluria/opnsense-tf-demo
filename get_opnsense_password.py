#!/usr/bin/env python3
"""
Simple wrapper to get OPNsense password.
Usage: python get_opnsense_password.py
"""

import os
import sys
from pathlib import Path

# Import from the main module
from get_instance_password import get_instance_password


def main():
    # Configuration
    instance_name = "opnsense"
    private_key_path = "sshkey"

    # Auto-detect cloud from clouds.yaml or use environment variable
    cloud_name = os.environ.get('OS_CLOUD', 'PCP-XDCZUTY-dc4-a')

    # Verify the private key exists
    if not Path(private_key_path).exists():
        print(f"Error: Private key '{private_key_path}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        password = get_instance_password(cloud_name, instance_name, private_key_path)
        print(f"OPNsense root password: {password}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
