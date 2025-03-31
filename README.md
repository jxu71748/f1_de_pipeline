# Formula 1 Data Pipeline Project 🏎️ 🏎️ 🏎️ 

## Project Objective
This project is part of the DE Zoomcamp final capstone. The goal is to build a complete batch data pipeline using GCP, Terraform, Airflow, Spark, dbt, and Looker Studio. The dataset is from Kaggle and contains Formula 1 race data from 1950 to 2024.

## Tech Stack

![Tech Stack](https://github.com/jxu71748/f1-de-pipeline/assets/tech-stack-diagram.png)

- **Cloud**: Google Cloud Platform (GCS, BigQuery)
- **Infrastructure as Code**: Terraform
- **Workflow Orchestration**: Airflow
- **Processing Engine**: PySpark
- **Transformation**: dbt
- **Visualization**: Looker Studio
- **Language**: Python


## Dashboar

### 1. Race Hosting Analysis
- Top 10 Countries by Races Hosted
- Pie Chart of Country Distribution
- Total Races & Countries KPIs

![Race Count](assets/races & countries.png)

### 2. Constructor Performance
- **Total Points per Year** (Line Chart)
- **Top 5 Winning Constructors** (Bar Chart)

![Constructor Stats](assets/constructor_stats.png)

### 3. Driver Fastest Lap Records
- Fastest lap time per driver by year (Scatter Plot)

![Fastest Lap](assets/Driver Fastest Lap Records.png)


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

### Docker Setup

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
FYI 😊, this `scripts` folder is the one that underneath our project.
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

#### Core Models

| Model                    | Description                                       |
|-------------------------|---------------------------------------------------|
| `fct_constructor_stats` | Total points & wins per constructor by year       |
| `fct_driver_fastest_lap`| Fastest lap time per driver by year               |
| `fct_race_count_by_country` | Number of races hosted per country           |

#### Running the dbt pipeline

FYI 😊, providing a helper script to run dbt pipeline & generate docs in one step:
```bash
bash run_dbt_and_docs.sh
```

Then to preview the generated documentation:
```bash
cd dbt
dbt docs serve --port 8081
```
Serving docs at `http://localhost:8081 ...`
✌️✌️✌️

### Author
Built by Jingwen Xu.





