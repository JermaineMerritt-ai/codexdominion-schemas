output "gclb_ip" {
	description = "Global static IP for Google HTTPS Load Balancer"
	value       = module.gcp_gclb_ingress.gclb_ip
}

output "afd_endpoint" {
	description = "Azure Front Door endpoint hostname"
	value       = module.azure_front_door.afd_endpoint
}

output "db_connection_string" {
	description = "Connection string for the Google SQL database"
	value       = "postgres://${var.db_user}:${var.db_pass}@${google_sql_database_instance.db.connection_name}"
	sensitive   = true
}

output "signals_service_url" {
	description = "URL of the deployed Cloud Run signals service"
	value       = google_cloud_run_service.signals.status[0].url
}

output "cloudflare_zone_id" {
	description = "Zone ID for Cloudflare DNS management"
	value       = cloudflare_zone.codex.zone_id
}
output "afd_endpoint" {
	description = "Front Door endpoint hostname"
	value       = azurerm_frontdoor_frontend_endpoint.endpoint.host_name
}

output "afd_custom_domain" {
	description = "Front Door custom domain hostname"
	value       = azurerm_frontdoor_custom_domain.www_domain.host_name
}
output "gclb_ip" {
	description = "Global static IP for the GCLB"
	value       = google_compute_global_address.gclb_ip.address
}
###############################
# outputs.tf for Codex Dominion Multi-Cloud Infrastructure
###############################

output "gclb_ip" {
	description = "Global static IP for Google HTTPS Load Balancer"
	value       = module.gcp_gclb_ingress.gclb_ip
}

output "afd_endpoint" {
	description = "Azure Front Door endpoint hostname"
	value       = module.azure_front_door.afd_endpoint
}
