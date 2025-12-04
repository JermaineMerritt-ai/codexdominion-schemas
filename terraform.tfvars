# terraform.tfvars
# Terraform configuration for Codex Dominion

# Project and region (aligned with variables.tf)
gcp_project_id = "codex-dominion-prod"
gcp_region     = "us-central1"

# Cloud SQL settings
db_tier = "db-f1-micro"
db_user = "codex_user"
# db_pass - Set via environment variable: export TF_VAR_db_pass="your_secure_password"

# Signals Engine container image
signals_image = "gcr.io/codex-dominion-prod/codex-signals:latest"

# Cloudflare DNS automation
# cloudflare_api_token - Set via environment variable: export TF_VAR_cloudflare_api_token="your_token"
server_ip = "98.19.211.133"
