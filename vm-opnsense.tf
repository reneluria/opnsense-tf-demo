resource "openstack_networking_port_v2" "opnsense_internal" {
  name           = "opnsense_internal"
  network_id     = openstack_networking_network_v2.internal.id
  admin_state_up = "true"
  fixed_ip {
    subnet_id  = openstack_networking_subnet_v2.internal_1.id
    ip_address = "192.168.120.1"
  }
  security_group_ids = [openstack_networking_secgroup_v2.opnsense_internal.id]
  allowed_address_pairs {
    ip_address = "0.0.0.0/0"
  }
}

resource "openstack_networking_port_v2" "opnsense_external" {
  name               = "opnsense_external"
  network_id         = data.openstack_networking_network_v2.external.id
  admin_state_up     = "true"
  security_group_ids = [openstack_networking_secgroup_v2.opnsense_external.id]
}

data "openstack_images_image_v2" "opnsense" {
  name = "OPNsense"
}

resource "openstack_blockstorage_volume_v3" "opnsense" {
  name     = "opnsense"
  size     = 20
  image_id = data.openstack_images_image_v2.opnsense.id
}

resource "openstack_compute_instance_v2" "opnsense" {
  name        = "opnsense"
  flavor_name = "a2-ram4-disk0"
  key_pair    = openstack_compute_keypair_v2.keypair.name

  block_device {
    uuid             = openstack_blockstorage_volume_v3.opnsense.id
    boot_index       = 0
    source_type      = "volume"
    destination_type = "volume"
  }

  network {
    port = openstack_networking_port_v2.opnsense_external.id
  }

  network {
    port = openstack_networking_port_v2.opnsense_internal.id
  }
}


