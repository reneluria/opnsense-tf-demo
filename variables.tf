variable "external_network" {
  type    = string
  default = "ext-net1"
}

variable "admin_prefixes" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}
