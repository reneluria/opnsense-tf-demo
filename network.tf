data "openstack_networking_network_v2" "external" {
  name = var.external_network
}

resource "openstack_networking_network_v2" "internal" {
  name           = "internal"
  admin_state_up = "true"
}

resource "openstack_networking_subnet_v2" "internal_1" {
  name            = "internal_1"
  network_id      = openstack_networking_network_v2.internal.id
  cidr            = "192.168.120.0/24"
  ip_version      = 4
  dns_nameservers = ["192.168.120.1"]
}
