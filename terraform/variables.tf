variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-west1"
}

variable "bucket_name" {
  type = string
}

variable "bq_dataset" {
  type = string
}
