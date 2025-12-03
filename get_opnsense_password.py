#!/usr/bin/env python3
# Copyright (C) 2024 demo-opensense contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
