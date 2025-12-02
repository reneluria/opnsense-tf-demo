output "opnsense_ip" {
  value = openstack_networking_port_v2.opnsense_external.all_fixed_ips
}

output "basic_ip" {
  value = openstack_compute_instance_v2.basic.access_ip_v4
}
