terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.113"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.33"
    }
  }
}

# Option A: Service Account Key (local/dev)
provider "google" {
  project     = var.gcp_project_id
  region      = var.gcp_region
  credentials = var.gcp_sa_key_file != "" ? file(var.gcp_sa_key_file) : null
}

# Option B: Workload Identity Federation (GitHub Actions)
provider "google" {
  alias                       = "wif"
  project                     = var.gcp_project_id
  region                      = var.gcp_region
  impersonate_service_account = var.gcp_service_account_email
  access_token                = var.github_oidc_token
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

provider "kubernetes" {
  host                   = var.k8s_host
  client_certificate     = base64decode(var.k8s_client_certificate)
  client_key             = base64decode(var.k8s_client_key)
  cluster_ca_certificate = base64decode(var.k8s_cluster_ca_certificate)
}
