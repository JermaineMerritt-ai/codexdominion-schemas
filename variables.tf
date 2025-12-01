# Core GCP identifiers (already aligned with provider block)
variable "gcp_project_id" {
	type        = string
	description = "Google Cloud project ID for CodexDominion"
}

variable "gcp_region" {
	type        = string
	description = "Google Cloud region for resource deployment (e.g., us-central1)"
}

# Google SQL resources
variable "db_tier" {
	type        = string
	description = "Database tier (e.g., db-f1-micro, db-g1-small)"
}

variable "db_user" {
	type        = string
	description = "Database username for SQL instance"
}

variable "db_pass" {
	type        = string
	description = "Database password for SQL instance"
	sensitive   = true
}

# Cloud Run container image
variable "signals_image" {
	type        = string
	description = "Container image reference for the signals Cloud Run service"
}

# Cloudflare provider
variable "cloudflare_api_token" {
	type        = string
	description = "API token for Cloudflare DNS automation"
	sensitive   = true
}
# Cloudflare provider API token variable
variable "cloudflare_api_token" {
	type        = string
	description = "API token for Cloudflare provider"
	sensitive   = true
}
# Cloud Run container image variable
variable "signals_image" {
	type        = string
	description = "Container image for Google Cloud Run signals service"
}
# Google SQL Database variables
variable "db_tier" {
	type        = string
	description = "Tier for Google SQL instance (e.g., db-f1-micro, db-g1-small, etc.)"
}

variable "db_user" {
	type        = string
	description = "Username for Google SQL database user"
}

variable "db_pass" {
	type        = string
	description = "Password for Google SQL database user"
	sensitive   = true
}
# GCP
variable "gcp_project_id" {
	type = string
}

variable "gcp_region" {
	type = string
}

# Service Account Key path (for local/dev)
variable "gcp_sa_key_file" {
	type        = string
	description = "Path to JSON key file for service account"
	default     = ""
}

# WIF (for GitHub Actions)
variable "gcp_service_account_email" {
	type        = string
	description = "Service account email (e.g. terraform-deployer@PROJECT.iam.gserviceaccount.com)"
}
variable "gcp_wif_provider_name" {
	type        = string
	description = "Workload Identity Federation provider name (projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL/providers/PROVIDER)"
}
variable "github_oidc_token" {
	type        = string
	description = "OIDC token from GitHub Actions"
	default     = ""
}

# Azure
variable "azure_subscription_id" {
	type = string
}
variable "azure_resource_group" {
	type = string
}
variable "afd_profile_name" {
	type = string
}
variable "afd_endpoint_name" {
	type = string
}

# Domains
variable "domain_apex" {
	type = string
}
variable "domain_www" {
	type = string
}

# Kubernetes
variable "k8s_namespace" {
	type    = string
	default = "default"
}
# For GCP Workload Identity Federation (WIF) and GitHub OIDC
variable "gcp_service_account_email" {
	type        = string
	description = "GCP service account email for impersonation via WIF"
}

variable "gcp_wif_provider_name" {
	type        = string
	description = "GCP Workload Identity Federation provider name"
}

variable "github_oidc_token" {
	type        = string
	description = "GitHub OIDC token for federated authentication"
}
# For Google provider credentials
variable "gcp_sa_key_file" {
	type        = string
	description = "Path to GCP service account JSON key file"
}
# For GCP GCLB Ingress module (compatibility)
variable "domain_apex" {
	type        = string
	description = "Apex domain for GCP ingress (e.g., codexdominion.app)"
}

variable "domain_www" {
	type        = string
	description = "WWW domain for GCP ingress (e.g., www.codexdominion.app)"
}

variable "k8s_namespace" {
	type        = string
	default     = "default"
	description = "Kubernetes namespace for GKE resources"
}
# For GCP GCLB Ingress module
variable "domain_apex" {
	type        = string
	description = "Apex domain for GCP ingress (e.g., codexdominion.app)"
}

variable "domain_www" {
	type        = string
	description = "WWW domain for GCP ingress (e.g., www.codexdominion.app)"
}

# For Azure Front Door module
variable "afd_profile_name" {
	type        = string
	description = "Azure Front Door profile name"
}

variable "afd_endpoint_name" {
	type        = string
	description = "Azure Front Door endpoint name"
}

variable "origin_host" {
	type        = string
	description = "Host for Azure Front Door origin (e.g., apex domain served by GCLB)"
}
###############################
# variables.tf for Codex Dominion Multi-Cloud Infrastructure
###############################

# GCP
variable "gcp_project_id" {
	type = string
	description = "GCP project ID"
}

variable "gcp_region" {
	type = string
	description = "GCP region (e.g., us-central1)"
}

variable "codexdominion_domain" {
	type = string
	description = "Apex domain (e.g., codexdominion.app)"
}

variable "codexdominion_www_domain" {
	type = string
	description = "WWW domain (e.g., www.codexdominion.app)"
}

# GKE/Kubernetes
variable "k8s_host" {
	type = string
	description = "Kubernetes API server endpoint"
}

variable "k8s_client_certificate" {
	type = string
	description = "Base64-encoded client certificate"
}

variable "k8s_client_key" {
	type = string
	description = "Base64-encoded client key"
}

variable "k8s_cluster_ca_certificate" {
	type = string
	description = "Base64-encoded cluster CA certificate"
}

variable "k8s_namespace" {
	type    = string
	default = "default"
	description = "Kubernetes namespace"
}

# Azure
variable "azure_subscription_id" {
	type = string
	description = "Azure subscription ID"
}

variable "azure_resource_group" {
	type = string
	description = "Azure resource group name"
}

variable "azure_location" {
	type    = string
	default = "eastus"
	description = "Azure region/location"
}

variable "azure_afd_profile_name" {
	type = string
	description = "Azure Front Door profile name"
}

variable "azure_afd_endpoint_name" {
	type = string
	description = "Azure Front Door endpoint name"
}

# Optional: Add more variables for module integration as needed
