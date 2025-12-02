# Demo opnsense

## Intro

Terraform / opentofu reecepie to setup a self-service network for isolated VMs and OPNsense
Infomaniak public cloud service.

[https://www.infomaniak.com/en/hosting/public-cloud](https://www.infomaniak.com/en/hosting/public-cloud)
[https://opnsense.org/](https://opnsense.org/)

## Description

VMs like [vm-basic](vm-basic.tf) are in a self service private network
in our example, 192.168.120.0/24

They get `192.168.0.1` as default gateway and DNS server via DHCP

An OPNsense instance is deployed, with one interface attached to external public network
and one interface to the private network.

It is accessible on port 80, 443 on the `admin_prefixes` defined list,
and from anywhere via ICMP or port 52180 for wireguard.

## Infra setup

Setup openstack credentials, like with a `clouds.yaml` file, then

```shell
tofu init
tofu apply
```

This will create everything needed.

## Usage

Once setup, you have a working OPNsense instance and a local VM

To access the OPNsense get ip from outputs (opnsense_ip) and open your browser
login is root, [and password to get here](https://docs.infomaniak.cloud/tutorials/firewall/opnsense/#retrieve-administrator-password)

Setup the Wireguard in vpn/wireguard and appropriate rules

