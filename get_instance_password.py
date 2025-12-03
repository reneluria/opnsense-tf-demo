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
Get instance password from OpenStack using clouds.yaml credentials.
Equivalent to: nova get-password <instance_name> <private_key_path>
"""

import argparse
import sys
from pathlib import Path

import openstack
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def decrypt_password(encrypted_password: str, private_key_path: str) -> str:
    """
    Decrypt the password using the private SSH key.

    Args:
        encrypted_password: Base64 encoded encrypted password
        private_key_path: Path to the private SSH key file

    Returns:
        Decrypted password string
    """
    import base64

    # Read the private key
    with open(private_key_path, 'rb') as key_file:
        loaded_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    # Ensure it's an RSA key (OpenStack uses RSA for password encryption)
    if not isinstance(loaded_key, rsa.RSAPrivateKey):
        raise ValueError("Private key must be an RSA key")

    # Decode the base64 encrypted password
    encrypted_bytes = base64.b64decode(encrypted_password)

    # Decrypt using PKCS1v15 padding (same as OpenStack uses)
    decrypted = loaded_key.decrypt(
        encrypted_bytes,
        padding.PKCS1v15()
    )

    return decrypted.decode('utf-8')


def get_instance_password(cloud_name: str, instance_name: str, private_key_path: str) -> str:
    """
    Get and decrypt the password for an OpenStack instance.

    Args:
        cloud_name: Name of the cloud from clouds.yaml
        instance_name: Name or ID of the instance
        private_key_path: Path to the private SSH key used to decrypt

    Returns:
        Decrypted password string
    """
    # Connect to OpenStack
    conn = openstack.connect(cloud=cloud_name)

    # Find the server
    server = conn.compute.find_server(instance_name)
    if not server:
        raise ValueError(f"Server '{instance_name}' not found")

    # Get the encrypted password
    password_data = conn.compute.get_server_password(server)

    # The API returns the encrypted password directly as a string
    if not password_data:
        raise ValueError(
            f"No password available for instance '{instance_name}'. "
            "The instance may not have password retrieval enabled."
        )

    # Decrypt and return
    return decrypt_password(password_data, private_key_path)


def main():
    parser = argparse.ArgumentParser(
        description='Get instance password from OpenStack (equivalent to nova get-password)'
    )
    parser.add_argument(
        'instance',
        help='Instance name or ID'
    )
    parser.add_argument(
        'private_key',
        help='Path to private SSH key for decryption'
    )
    parser.add_argument(
        '--cloud',
        default=None,
        help='Cloud name from clouds.yaml (defaults to OS_CLOUD env var or first cloud)'
    )

    args = parser.parse_args()

    # Verify private key exists
    if not Path(args.private_key).exists():
        print(f"Error: Private key file not found: {args.private_key}", file=sys.stderr)
        sys.exit(1)

    try:
        # Get cloud name from args or environment
        cloud_name = args.cloud
        if not cloud_name:
            import os
            cloud_name = os.environ.get('OS_CLOUD')

        if not cloud_name:
            # Try to get first cloud from clouds.yaml
            clouds = openstack.config.loader.OpenStackConfig().get_all()
            if clouds:
                cloud_name = clouds[0].name
            else:
                print("Error: No cloud specified and no clouds found in clouds.yaml", file=sys.stderr)
                sys.exit(1)

        password = get_instance_password(cloud_name, args.instance, args.private_key)
        print(password)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
