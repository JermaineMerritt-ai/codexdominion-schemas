terraform {
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.40" }
  }
}
provider "google" {
  project = var.google_project
}

variable "google_project" { type = string }
variable "google_zone"    { type = string }  # managed zone name, e.g., "codexdominion-app"
variable "records" {
  type = map(object({
    type    = string    # "A" or "CNAME"
    name    = string    # e.g., "faith.codexdominion.app."
    ttl     = number
    rrdatas = list(string) # IPs or hostnames
  }))
  validation {
    condition = alltrue([
      for k, v in var.records : contains(["A", "CNAME"], v.type)
    ])
    error_message = "Only A and CNAME records are supported."
  }
}

resource "google_dns_record_set" "subdomains" {
  for_each    = var.records
  name        = each.value.name
  type        = each.value.type
  ttl         = each.value.ttl
  managed_zone = var.google_zone
  rrdatas     = each.value.rrdatas
}

output "record_names" {
  value = [for k, v in google_dns_record_set.subdomains : v.name]
}

output "record_details" {
  value = [for k, v in google_dns_record_set.subdomains : {
    name    = v.name
    type    = v.type
    ttl     = v.ttl
    rrdatas = v.rrdatas
  }]
}

# ---
# NOTE: For production, use a remote backend for state storage (e.g., GCS, S3, etc.)
# Example:
# terraform {
#   backend "gcs" {
#     bucket  = "..."
#     prefix  = "google-dns/state"
#   }
# }
