# Formula 1 Data Pipeline Project 🏎️ 🏎️ 🏎️ 

## Project Objective
This project is part of the DE Zoomcamp course final project. The goal is to build a complete batch data pipeline using GCP, Terraform, Airflow, and Spark. The dataset is from Kaggle and contains Formula 1 race data from 1950 to 2024.

## Tools Used
- Cloud: Google Cloud Platform (GCS & BigQuery)
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Airflow
- Batch processing: PySpark for data transformation
- Visualization: Google Data Studio
- Python for scripting (data download, upload, transformation)

## Project Overview

### Infrastructure Setup with Terraform

This project uses Terraform to provision the required GCP resources:

- A Google Cloud Storage bucket to store raw files
- A BigQuery dataset to hold processed data

Make sure you have a GCP project and service account key before running Terraform.

#### Run Terraform
```bash
cd terraform/
terraform init
terraform plan
terraform apply
```
After this, you’ll have:
1. A GCS bucket like gs://f1-de-bucket
2. A BigQuery dataset like f1_data

### Setup Google Cloud Credentials
To run scripts that interact with GCS or BigQuery, make sure you set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your GCP service account key.

You can add the following line to your `.zshrc` or `.bashrc` file to make it permanent:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/path/to/terraform/credentials/terraform-key.json"
export GOOGLE_CLOUD_PROJECT="your-projectID"
```
Now, you don't have to run the credentials everytime you need it.

### Airflow Ingestion DAG
This DAG automates the first part of the pipeline:
- Download Formula 1 data from Kaggle
- Upload all CSV files to GCS under the `raw/` folder

To run manually:
```bash
airflow dags trigger f1_ingestion_dag
```


## Current Progress
- ✅ Downloaded raw data from Kaggle
- ✅ Created GCS bucket and BigQuery dataset using Terraform
- 🔜 Upload raw CSV files to GCS via Python
- 🔜 Build Airflow DAGs for ingestion and transformation
- 🔜 Create a dashboard with race results insights

## Folder Structure

