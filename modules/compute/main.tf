terraform {
  required_providers {
    ionoscloud = { source = "ionos-cloud/ionoscloud", version = "~> 6.0" }
  }
}

provider "ionoscloud" {
  username = var.ionos_username
  password = var.ionos_password
}

variable "ionos_username" {
  type      = string
  sensitive = true
}

variable "ionos_password" {
  type      = string
  sensitive = true
}

variable "dc_name"       { type = string }    # e.g., codex-prod-dc
variable "prefix"        { type = string }
variable "env"           { type = string }
variable "domain_fqdn"   { type = list(string) }  # e.g., ["faith.example.com","children.example.com","lifestyle.example.com"]
variable "instance_size" { type = string }    # e.g., "C8" or "S8" per IONOS sizes
variable "image"         { type = string }    # e.g., "Ubuntu-22.04"
variable "ssh_pubkey"    { type = string }
variable "location" {
  type    = string
  default = "de/fra"
}
variable "tags" {
  type    = map(string)
  default = {}
}

locals {
  sizes = {
    "C8" = { cores = 8, ram = 16384 }
    "S8" = { cores = 4, ram = 8192 }
    # Add more sizes as needed
  }
}

resource "ionoscloud_datacenter" "dc" {
  name        = var.dc_name
  location    = var.location
  description = "CodexDominion ${var.env} datacenter"

}

resource "ionoscloud_lan" "lan" {
  datacenter_id = ionoscloud_datacenter.dc.id
  name          = "${var.prefix}-${var.env}-lan"
  public        = true

}

resource "ionoscloud_ipblock" "ipb" {
  location = var.location
  size     = 3
  name     = "${var.prefix}-${var.env}-ipblock"

}

resource "ionoscloud_server" "wp" {
  datacenter_id = ionoscloud_datacenter.dc.id
  name          = "${var.prefix}-${var.env}-wp"
  cores         = local.sizes[var.instance_size].cores
  ram           = local.sizes[var.instance_size].ram
  availability_zone = "ZONE_1"
  cpu_family    = "AMD_OPTERON"
  boot_volume {
    name       = "${var.prefix}-${var.env}-boot"
    size       = 60
    image_name = var.image
    image_password = "ChangeMe!"
    ssh_keys   = [var.ssh_pubkey]
    disk_type  = "SSD"
  }
  nic {
    lan     = ionoscloud_lan.lan.id
    name    = "wan"
    dhcp    = true
    ips     = slice(ionoscloud_ipblock.ipb.ips, 0, 1)
  }

}

resource "ionoscloud_application_loadbalancer" "alb" {
  datacenter_id = ionoscloud_datacenter.dc.id
  name          = "${var.prefix}-${var.env}-alb"
  ips           = slice(ionoscloud_ipblock.ipb.ips, 1, 2)
  listener {
    name        = "https"
    protocol    = "HTTPS"
    port        = 443
    client_timeout = 60
  }
  target_group {
    name = "${var.prefix}-${var.env}-tg"
    health_check {
      check_interval = 10
      retries        = 3
      timeout        = 5
      method         = "GET"
      path           = "/health"
    }
  }

}

output "wp_public_ip" {
  value = ionoscloud_server.wp.nic[0].ips[0]
}
