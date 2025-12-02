data "openstack_images_image_v2" "debian" {
  name = "Debian 13 trixie"
}

resource "openstack_compute_instance_v2" "basic" {
  name            = "basic"
  image_id        = data.openstack_images_image_v2.debian.id
  flavor_name     = "a1-ram2-disk20-perf1"
  key_pair        = openstack_compute_keypair_v2.keypair.name
  security_groups = [openstack_networking_secgroup_v2.opnsense_internal.name]

  network {
    uuid = openstack_networking_network_v2.internal.id
  }
}
