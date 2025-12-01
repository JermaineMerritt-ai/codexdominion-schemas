# terraform.tfvars
# Terraform configuration for Codex Dominion

# Project and region
project_id = "codex-dominion-prod"
region     = "us-central1"

# Cloud SQL settings
db_tier = "db-f1-micro"
db_user = "codex_user"
db_pass = "codex_pass"   # replace with a secure secret in production

# Signals Engine container image
signals_image = "gcr.io/codex-dominion-prod/codex-signals:latest"

# Cloudflare DNS automation
cloudflare_api_token = "WuKuLdijG-JVTyTqH8SA7K3rOTBOB8DAePOd14On"
server_ip = "98.19.211.133"