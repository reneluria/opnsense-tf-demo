resource "openstack_compute_keypair_v2" "keypair" {
  name = "keypair"
}

resource "local_file" "sshkey_priv" {
  content         = openstack_compute_keypair_v2.keypair.private_key
  filename        = "${path.module}/sshkey"
  file_permission = "0600"
}

resource "local_file" "sshkey_pub" {
  content         = openstack_compute_keypair_v2.keypair.public_key
  filename        = "${path.module}/sshkey.pub"
  file_permission = "0644"
}
