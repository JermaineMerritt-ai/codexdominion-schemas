# variables.tf

variable "project_id" {
  description = "The GCP project ID where Codex Dominion will be deployed"
  type        = string
}

variable "region" {
  description = "Default region for resources"
  type        = string
  default     = "us-central1"
}

variable "db_tier" {
  description = "Machine tier for Cloud SQL Postgres"
  type        = string
  default     = "db-f1-micro"
}

variable "db_user" {
  description = "Database username"
  type        = string
  default     = "codex_user"
}

variable "db_pass" {
  description = "Database password (use Secret Manager in production)"
  type        = string
  default     = "codex_pass"
  sensitive   = true
}

variable "signals_image" {
  description = "Container image for Codex Signals Engine"
  type        = string
}

variable "cloudflare_api_token" {
  description = "API token for Cloudflare provider"
  type        = string
  sensitive   = true
}

variable "zone_id" {
  description = "Cloudflare Zone ID for CodexDominion.app"
  type        = string
}

variable "server_ip" {
  description = "IP address for A records (Codex Dominion server)"
  type        = string
}