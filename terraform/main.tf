provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "f1_bucket" {
  name     = var.bucket_name
  location = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "f1_dataset" {
  dataset_id = var.bq_dataset
  location   = var.region
}
