# Formula 1 Data Pipeline Project 🏎️ 🏎️ 🏎️ 

## Project Objective
This project is part of the DE Zoomcamp course final project. The goal is to build a complete batch data pipeline using GCP, Terraform, Airflow, and Spark. The dataset is from Kaggle and contains Formula 1 race data from 1950 to 2024.

## Tools Used
- Cloud: Google Cloud Platform (GCS & BigQuery)
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Airflow
- Batch processing: PySpark + dbt for data transformation
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

---
### Setup Google Cloud Credentials
To run scripts that interact with GCS or BigQuery, make sure you set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your GCP service account key.

You can add the following line to your `.zshrc` or `.bashrc` file to make it permanent:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/path/to/terraform/credentials/terraform-key.json"
export GOOGLE_CLOUD_PROJECT="your-projectID"
```
Now, you don't have to run the credentials everytime you need it.

Also, this project uses GOOGLE_APPLICATION_CREDENTIALS environment variable to securely authenticate GCS clients. Please ensure you have the proper key mounted and environment set in `docker-compose.yaml`.

---
### Airflow Ingestion DAG
This DAG automates the first part of the pipeline:
- Download Formula 1 data from Kaggle
- Upload all CSV files to GCS under the `raw/` folder

Use pip to install airflow:
```bash
pip install apache-airflow
```

---

### Docker Setup (Updated)

Make sure you're in the `docker/` directory before running the commands below.

#### 1. Clean up existing containers (optional)
If you've previously started containers or want a fresh setup:
```bash
cd docker
docker compose down --volumes --remove-orphans
```

#### 2. Build custom Airflow image with Spark, PostgreSQL, Kaggle support
This builds the Airflow image with all tools pre-installed and ready to go:
- OpenJDK + Spark (for PySpark data transformation)
- PostgreSQL (Airflow metadata DB)
- Kaggle CLI (to download datasets)
- GCS credentials (for uploading data to Google Cloud)
- Local volume mounts for raw_data, transformed Parquet files, and DAGs

```bash
docker compose build
```
This may take a few minutes the first time. Once built, you can launch with `docker compose up -d`.

#### 3. Initialize Airflow database and create admin user
```bash
docker compose up airflow-init
```

#### 4. Start all Airflow and Postgres services
```bash
docker compose up -d
```

Check if everything is running:
```bash
docker ps
```

#### 5. Access Airflow UI
Go to: [http://localhost:8080](http://localhost:8080)

Log in with:
- **Username**: `admin`
- **Password**: `admin`

#### 6. (Optional) Stop everything
```bash
docker compose down
```

#### 7. (Optional) Restart after reboot
```bash
docker compose up -d
```

---

### Spark Notes
- Spark is installed in `/opt/spark`
- To manually test:
```bash
docker exec -it airflow-webserver bash
/opt/spark/bin/spark-submit --version
```

---

### DAGs
You can now run:
- `f1_ingestion_dag`: Downloads data from Kaggle and uploads raw CSVs to GCS (Bronze)
- `f1_transform_dag`: Transforms raw CSVs to cleaned Parquet using PySpark (Silver)
- `f1_upload_silver_dag`: Uploads cleaned Parquets to GCS (Silver)

---
### Load Silver Data (Parquet) from GCS to BigQuery

Once you've uploaded the cleaned Parquet files to `gs://f1-de-bucket/silver/`, run the following script to load them into BigQuery:

```bash
cd scripts
bash load_all_parquet_to_bq.sh
```
Make sure your GCP credentials are properly configured and the target dataset (f1_data) already exists.

---
### dbt Setup & Usage

This project uses [dbt](https://www.getdbt.com/) to transform data in BigQuery.

#### Requirements

Make sure you have the following Python packages installed:

```bash
pip install dbt-core dbt-bigquery
```

#### Running dbt

Once you're in the `dbt/` folder:

```bash
# Install any required packages
dbt deps

# Clean previous build files (optional but good habit)
dbt clean

# Run the models (we’re using views for the staging layer)
dbt run

# (Optional) Run tests
dbt test
```




### Next Steps
Set up dbt models (core)
Visualize results in dashboards (Google Data Studio).

---



