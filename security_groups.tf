resource "openstack_networking_secgroup_v2" "opnsense_internal" {
  name        = "opnsense_internal"
  description = "Security group on internal interface for opnsense"
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_internal_icmp" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "icmp"
  security_group_id = openstack_networking_secgroup_v2.opnsense_internal.id
  remote_group_id   = openstack_networking_secgroup_v2.opnsense_internal.id
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_internal_tcp" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  security_group_id = openstack_networking_secgroup_v2.opnsense_internal.id
  remote_group_id   = openstack_networking_secgroup_v2.opnsense_internal.id
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_internal_udp" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "udp"
  security_group_id = openstack_networking_secgroup_v2.opnsense_internal.id
  remote_group_id   = openstack_networking_secgroup_v2.opnsense_internal.id
}

resource "openstack_networking_secgroup_v2" "opnsense_external" {
  name        = "opnsense_external"
  description = "Security group on external interface for opnsense"
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_external_icmp" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "icmp"
  security_group_id = openstack_networking_secgroup_v2.opnsense_external.id
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_external_http" {
  count             = length(var.admin_prefixes)
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 80
  port_range_max    = 80
  remote_ip_prefix  = var.admin_prefixes[count.index]
  security_group_id = openstack_networking_secgroup_v2.opnsense_external.id
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_external_https" {
  count             = length(var.admin_prefixes)
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 443
  port_range_max    = 443
  remote_ip_prefix  = var.admin_prefixes[count.index]
  security_group_id = openstack_networking_secgroup_v2.opnsense_external.id
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_external_wireguard_tcp" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 51820
  port_range_max    = 51820
  security_group_id = openstack_networking_secgroup_v2.opnsense_external.id
}

resource "openstack_networking_secgroup_rule_v2" "opnsense_external_wireguard_udp" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "udp"
  port_range_min    = 51820
  port_range_max    = 51820
  security_group_id = openstack_networking_secgroup_v2.opnsense_external.id
}
