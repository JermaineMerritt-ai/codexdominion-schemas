variable "IONOS_USERNAME" { type = string }
variable "IONOS_PASSWORD" {
  type      = string
  sensitive = true
}

variable "enable_google_dns" {
  type    = bool
  default = true
}
variable "google_project"    { type = string }
variable "google_zone"       { type = string }  # managed zone for codexdominion.app

locals {
  alb_ipv4 = module.compute.alb_ip
}

module "compute" {
  source          = "../../modules/ionos-compute"
  ionos_username  = var.IONOS_USERNAME
  ionos_password  = var.IONOS_PASSWORD
  prefix          = "codex"
  env             = "prod"
  image_name      = "Ubuntu-22.04"
  ssh_pubkey      = file("~/.ssh/id_rsa.pub")
  tags = {
    environment = "prod"
    owner       = "codex-dominion"
    module      = "compute"
  }
}

module "network" {
  source          = "../../modules/ionos-network"
  ionos_username  = var.IONOS_USERNAME
  ionos_password  = var.IONOS_PASSWORD
  zone            = "codexdominionsites.com" # if you use IONOS DNS elsewhere
  records         = {}
  tags = {
    environment = "prod"
    owner       = "codex-dominion"
    module      = "network"
  }
}

# Optional Azure backup module (toggle with variable)
# variable "enable_azure_backup" { type = bool default = false }
# module "azure_backup" {
#   count = var.enable_azure_backup ? 1 : 0
#   source = "../../modules/azure-backup"
#   ...
# }

module "google_dns" {
  count          = var.enable_google_dns ? 1 : 0
  source         = "../../modules/google-dns"
  google_project = var.google_project
  google_zone    = var.google_zone
  records = {
    faith = {
      type    = "A"
      name    = "faith.codexdominion.app."
      ttl     = 300
      rrdatas = [local.alb_ipv4]
    }
    kids = {
      type    = "A"
      name    = "kids.codexdominion.app."
      ttl     = 300
      rrdatas = [local.alb_ipv4]
    }
    lifestyle = {
      type    = "A"
      name    = "lifestyle.codexdominion.app."
      ttl     = 300
      rrdatas = [local.alb_ipv4]
    }
  }
}

output "dns_record_names" {
  value = length(module.google_dns) > 0 ? module.google_dns[0].record_names : []
}
output "dns_record_details" {
  value = length(module.google_dns) > 0 ? module.google_dns[0].record_details : []
}

output "alb_ipv4" {
  value = local.alb_ipv4
}

  value = module.google_dns[0].record_names
}

  value = module.google_dns[0].record_details
}

# ---
# NOTE: For production, use a remote backend for state storage (e.g., Azure Storage, S3, GCS, etc.)
# Example:
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "..."
#     storage_account_name = "..."
#     container_name       = "..."
#     key                  = "prod.tfstate"
#   }
# }
