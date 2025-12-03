# Codex Dominion Terraform Variables
# Cleaned and deduplicated

# GCP Configuration
variable "gcp_project_id" {
  type        = string
  description = "Google Cloud project ID for CodexDominion"
}

variable "gcp_region" {
  type        = string
  description = "Google Cloud region for resource deployment (e.g., us-central1)"
  default     = "us-central1"
}

# Database Configuration
variable "db_tier" {
  type        = string
  description = "Database tier (e.g., db-f1-micro, db-g1-small)"
  default     = "db-f1-micro"
}

variable "db_user" {
  type        = string
  description = "Database username for SQL instance"
  default     = "codex_user"
}

variable "db_pass" {
  type        = string
  description = "Database password for SQL instance"
  sensitive   = true
}

# Cloud Run
variable "signals_image" {
  type        = string
  description = "Container image reference for the signals Cloud Run service"
  default     = "gcr.io/codex-dominion-prod/signals:latest"
}

# Cloudflare
variable "cloudflare_api_token" {
  type        = string
  description = "API token for Cloudflare DNS automation"
  sensitive   = true
}

# Server Configuration
variable "server_ip" {
  type        = string
  description = "IP address of the deployment server"
  default     = "98.19.211.133"
}

# GCP Service Account & Workload Identity
variable "gcp_sa_key_file" {
  type        = string
  description = "Path to JSON key file for service account (local/dev only)"
  default     = ""
}

variable "gcp_service_account_email" {
  type        = string
  description = "Service account email for Workload Identity Federation"
  default     = ""
}

variable "gcp_wif_provider_name" {
  type        = string
  description = "Workload Identity Federation provider name"
  default     = ""
}

variable "github_oidc_token" {
  type        = string
  description = "OIDC token from GitHub Actions"
  default     = ""
}

# Azure Configuration
variable "azure_subscription_id" {
  type        = string
  description = "Azure subscription ID"
  default     = ""
}

variable "azure_resource_group" {
  type        = string
  description = "Azure resource group name"
  default     = "codex-dominion-rg"
}

variable "azure_location" {
  type        = string
  description = "Azure region/location"
  default     = "eastus"
}

variable "afd_profile_name" {
  type        = string
  description = "Azure Front Door profile name"
  default     = "codex-afd-profile"
}

variable "afd_endpoint_name" {
  type        = string
  description = "Azure Front Door endpoint name"
  default     = "codex-afd-endpoint"
}

# Domain Configuration
variable "domain_apex" {
  type        = string
  description = "Apex domain (e.g., codexdominion.app)"
  default     = "codexdominion.app"
}

variable "domain_www" {
  type        = string
  description = "WWW domain (e.g., www.codexdominion.app)"
  default     = "www.codexdominion.app"
}

variable "codexdominion_domain" {
  type        = string
  description = "Apex domain (alias for domain_apex)"
  default     = "codexdominion.app"
}

variable "codexdominion_www_domain" {
  type        = string
  description = "WWW domain (alias for domain_www)"
  default     = "www.codexdominion.app"
}

# Kubernetes Configuration
variable "k8s_namespace" {
  type        = string
  description = "Kubernetes namespace for GKE resources"
  default     = "default"
}

variable "k8s_host" {
  type        = string
  description = "Kubernetes API server endpoint"
  default     = ""
}

variable "k8s_client_certificate" {
  type        = string
  description = "Base64-encoded client certificate"
  default     = ""
  sensitive   = true
}

variable "k8s_client_key" {
  type        = string
  description = "Base64-encoded client key"
  default     = ""
  sensitive   = true
}

variable "k8s_cluster_ca_certificate" {
  type        = string
  description = "Base64-encoded cluster CA certificate"
  default     = ""
  sensitive   = true
}

# Azure Front Door Origin
variable "origin_host" {
  type        = string
  description = "Host for Azure Front Door origin (e.g., apex domain served by GCLB)"
  default     = ""
}
