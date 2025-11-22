# outputs.tf

output "cloud_sql_connection_name" {
  description = "Connection string for Cloud SQL Postgres"
  value       = google_sql_database_instance.codex_ledger.connection_name
}

output "cloud_sql_db_name" {
  description = "Codex Ledger database name"
  value       = google_sql_database.codex.name
}

output "cloud_storage_bucket" {
  description = "Bucket for capsule artifacts"
  value       = google_storage_bucket.codex_artifacts.url
}

output "signals_service_url" {
  description = "Public URL for Codex Signals Engine (Cloud Run)"
  value       = google_cloud_run_service.signals.status[0].url
}

output "dawn_dispatch_job" {
  description = "Cloud Scheduler job for daily dawn dispatch"
  value       = google_cloud_scheduler_job.dawn_dispatch.name
}