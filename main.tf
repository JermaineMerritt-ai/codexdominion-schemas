# Codex Dominion - Simplified Main Terraform Configuration

terraform {
  required_version = ">= 1.6.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

# GCP Provider
provider "google" {
  project     = var.gcp_project_id
  region      = var.gcp_region
  credentials = var.gcp_sa_key_file != "" ? file(var.gcp_sa_key_file) : null
}

# Cloudflare Provider
provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# Google SQL Database Instance
resource "google_sql_database_instance" "db" {
  name             = "codex-dominion-db"
  database_version = "POSTGRES_15"
  region           = var.gcp_region

  settings {
    tier = var.db_tier

    ip_configuration {
      ipv4_enabled    = true
      authorized_networks {
        name  = "deployment-server"
        value = var.server_ip
      }
    }

    backup_configuration {
      enabled = true
    }
  }

  deletion_protection = false  # Set to true in production
}

# Database
resource "google_sql_database" "database" {
  name     = "codexdominion"
  instance = google_sql_database_instance.db.name
}

# Database User
resource "google_sql_user" "user" {
  name     = var.db_user
  instance = google_sql_database_instance.db.name
  password = var.db_pass
}

# Cloud Run Service
resource "google_cloud_run_service" "signals" {
  name     = "codex-signals"
  location = var.gcp_region

  template {
    spec {
      containers {
        image = var.signals_image
        
        env {
          name  = "DATABASE_URL"
          value = "postgresql://${var.db_user}:${var.db_pass}@${google_sql_database_instance.db.connection_name}/codexdominion"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Cloud Run IAM - Allow public access
resource "google_cloud_run_service_iam_member" "public" {
  service  = google_cloud_run_service.signals.name
  location = google_cloud_run_service.signals.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloudflare Zone (assumes zone already exists)
data "cloudflare_zone" "codex" {
  name = var.domain_apex
}

# Cloudflare DNS Record - Apex
resource "cloudflare_record" "apex" {
  zone_id = data.cloudflare_zone.codex.id
  name    = "@"
  content   = var.server_ip
  type    = "A"
  ttl     = 1  # Auto
  proxied = true
}

# Cloudflare DNS Record - WWW
resource "cloudflare_record" "www" {
  zone_id = data.cloudflare_zone.codex.id
  name    = "www"
  content   = var.server_ip
  type    = "A"
  ttl     = 1  # Auto
  proxied = true
}

# Outputs
output "db_connection_name" {
  description = "Google SQL instance connection name"
  value       = google_sql_database_instance.db.connection_name
}

output "signals_url" {
  description = "Cloud Run signals service URL"
  value       = google_cloud_run_service.signals.status[0].url
}

output "cloudflare_zone_id" {
  description = "Cloudflare zone ID"
  value       = data.cloudflare_zone.codex.id
}
