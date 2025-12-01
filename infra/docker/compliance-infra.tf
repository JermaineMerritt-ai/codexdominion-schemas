provider "docker" {}

# PostgreSQL container
resource "docker_container" "postgres" {
  name  = "postgres"
  image = "postgres:15"
  env = [
    "POSTGRES_USER=${var.pg_user}",
    "POSTGRES_PASSWORD=${var.pg_password}",
    "POSTGRES_DB=codexdominion"
  ]
  ports {
    internal = 5432
    external = 5432
  }
  volumes {
    container_path = "/var/lib/postgresql/data"
    host_path      = "/data/postgres"
  }
}

# MinIO container
resource "docker_container" "minio" {
  name  = "minio"
  image = "minio/minio:latest"
  command = ["server", "/data"]
  env = [
    "MINIO_ROOT_USER=${var.minio_user}",
    "MINIO_ROOT_PASSWORD=${var.minio_password}"
  ]
  ports {
    internal = 9000
    external = 9000
  }
  volumes {
    container_path = "/data"
    host_path      = "/data/minio"
  }
}
