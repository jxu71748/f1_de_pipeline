# Formula 1 Data Pipeline Project 🏎️ 🏎️ 🏎️ 
---
## Project Objective
This project is part of the DE Zoomcamp course final project. The goal is to build a complete batch data pipeline using GCP, Terraform, Airflow, and Spark. The dataset is from Kaggle and contains Formula 1 race data from 1950 to 2024.

---
## Tools Used
- Cloud: Google Cloud Platform (GCS & BigQuery)
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Airflow
- Batch processing: PySpark for data transformation
- Visualization: Google Data Studio
- Python for scripting (data download, upload, transformation)

---
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

#### 2. Build custom image with Spark support
This will build the Airflow image with OpenJDK + Spark pre-installed:
```bash
docker compose build
```

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

---

### Next Steps
Set up dbt models to move transformed Parquet (Silver) into BigQuery (Gold).
Visualize results in dashboards (e.g. Looker Studio or Google Data Studio).

---



