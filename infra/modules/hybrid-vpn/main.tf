terraform {
  required_providers {
    azurerm    = { source = "hashicorp/azurerm", version = "~> 3.108" }
    ionoscloud = { source = "ionos-cloud/ionoscloud", version = "~> 6.0" }
  }
}

provider "azurerm" {
  features {}
}
provider "ionoscloud" {
  username = var.ionos_username
  password = var.ionos_password
}

variable "azure_location"        { type = string }  # e.g., "eastus"
variable "azure_rg_name"         { type = string }
variable "azure_vnet_cidr"       { type = string }  # e.g., "10.50.0.0/16"
variable "azure_subnet_cidr"     { type = string }  # e.g., "10.50.0.0/24"
variable "ionos_private_cidr"    { type = string }  # e.g., "10.20.0.0/16"
variable "psk" {
  type      = string
  sensitive = true
}  # pre-shared key
variable "ionos_public_ip"       { type = string }  # IONOS public IP for VPN endpoint
variable "ionos_username"        { type = string }
variable "ionos_password" {
  type      = string
  sensitive = true
}
variable "log_analytics_workspace_id" { type = string }

resource "azurerm_resource_group" "rg" {
  name     = var.azure_rg_name
  location = var.azure_location
  tags = {
    environment = "production"
    owner       = "codex-dominion"
    module      = "hybrid-vpn"
  }
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.azure_rg_name}-vnet"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.azure_location
  address_space       = [var.azure_vnet_cidr]
  tags = {
    environment = "production"
    owner       = "codex-dominion"
    module      = "hybrid-vpn"
  }
}

resource "azurerm_subnet" "gateway_subnet" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [var.azure_subnet_cidr]
}

resource "azurerm_public_ip" "vpn_pip" {
  name                = "${var.azure_rg_name}-vpn-pip"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.azure_location
  allocation_method   = "Dynamic"
  sku                 = "Standard"
  tags = {
    environment = "production"
    owner       = "codex-dominion"
    module      = "hybrid-vpn"
  }
}

resource "azurerm_virtual_network_gateway" "azure_gw" {
  name                = "${var.azure_rg_name}-azure-gw"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.azure_location
  type                = "Vpn"
  vpn_type            = "RouteBased"
  active_active       = false
  enable_bgp          = false
  sku                 = "VpnGw1"
  ip_configuration {
    name                          = "gwip"
    public_ip_address_id          = azurerm_public_ip.vpn_pip.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway_subnet.id
  }
  tags = {
    environment = "production"
    owner       = "codex-dominion"
    module      = "hybrid-vpn"
  }
}

resource "azurerm_local_network_gateway" "ionos_peer" {
  name                = "${var.azure_rg_name}-ionos-peer"
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.azure_location
  gateway_address     = var.ionos_public_ip
  address_space       = [var.ionos_private_cidr]
  tags = {
    environment = "production"
    owner       = "codex-dominion"
    module      = "hybrid-vpn"
  }
}

resource "azurerm_virtual_network_gateway_connection" "hybrid" {
  name                           = "${var.azure_rg_name}-ionos-azure-conn"
  resource_group_name            = azurerm_resource_group.rg.name
  location                       = var.azure_location
  type                           = "IPsec"
  virtual_network_gateway_id     = azurerm_virtual_network_gateway.azure_gw.id
  local_network_gateway_id       = azurerm_local_network_gateway.ionos_peer.id
  shared_key                     = var.psk
  dpd_timeout_seconds            = 45
  ipsec_policy {
    ike_encryption   = "AES256"
    ike_integrity    = "SHA256"
    dh_group         = "DHGroup14"
    ipsec_encryption = "AES256"
    ipsec_integrity  = "SHA256"
    pfs_group        = "PFS2"
  }
  tags = {
    environment = "production"
    owner       = "codex-dominion"
    module      = "hybrid-vpn"
  }
}

output "azure_vpn_public_ip" {
  value = azurerm_public_ip.vpn_pip.ip_address
}

# ---
# NOTE: For production, use a remote backend for state storage (e.g., Azure Storage, S3, etc.)
# Example:
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "..."
#     storage_account_name = "..."
#     container_name       = "..."
#     key                  = "hybrid-vpn.tfstate"
#   }
# }
