# main.tf

terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Cloud SQL (Postgres)
resource "google_sql_database_instance" "codex_ledger" {
  name             = "codex-ledger"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = var.db_tier
    backup_configuration {
      enabled = true
    }
  }
}

resource "google_sql_database" "codex" {
  name     = "codex"
  instance = google_sql_database_instance.codex_ledger.name
}

resource "google_sql_user" "codex_user" {
  name     = var.db_user
  instance = google_sql_database_instance.codex_ledger.name
  password = var.db_pass
}

# Cloud Storage bucket for capsule artifacts
resource "google_storage_bucket" "codex_artifacts" {
  name          = "codex-artifacts-${var.project_id}"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
}

# Cloud Run service for Signals Engine
resource "google_cloud_run_service" "signals" {
  name     = "codex-signals"
  location = var.region

  template {
    spec {
      containers {
        image = var.signals_image
        resources {
          limits = {
            memory = "512Mi"
            cpu    = "1"
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Secret Manager entry for DB password
resource "google_secret_manager_secret" "db_pass" {
  secret_id = "codex-db-pass"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_pass_version" {
  secret      = google_secret_manager_secret.db_pass.id
  secret_data = var.db_pass
}

# Cloud Scheduler job for Dawn Dispatch
resource "google_cloud_scheduler_job" "dawn_dispatch" {
  name        = "dawn-dispatch"
  description = "Daily proclamation capsule"
  schedule    = "0 6 * * *"
  time_zone   = "America/New_York"

  http_target {
    uri         = google_cloud_run_service.signals.status[0].url
    http_method = "POST"
    body        = base64encode("{\"capsule\":\"dawn-dispatch\"}")
    headers = {
      "Content-Type" = "application/json"
    }
  }
}

# Cloudflare DNS automation for CodexDominion.app
provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

resource "cloudflare_record" "codex_root" {
  zone_id = var.zone_id
  name    = "@"
  type    = "A"
  value   = var.server_ip
    ttl     = 1
  proxied = true
}

resource "cloudflare_record" "codex_www" {
  zone_id = var.zone_id
  name    = "www"
  type    = "A"
  value   = var.server_ip
    ttl     = 1
  proxied = true
}