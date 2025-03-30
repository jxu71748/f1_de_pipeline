#!/bin/bash

set -e

echo "Starting bulk load of Parquet files from GCS to BigQuery (f1_data)..."

echo "Loading circuits..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.circuits gs://f1-de-bucket/silver/circuits.parquet/*.parquet

echo "Loading constructors..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.constructors gs://f1-de-bucket/silver/constructors.parquet/*.parquet

echo "Loading constructor_results..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.constructor_results gs://f1-de-bucket/silver/constructor_results.parquet/*.parquet

echo "Loading constructor_standings..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.constructor_standings gs://f1-de-bucket/silver/constructor_standings.parquet/*.parquet

echo "Loading driver_standings..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.driver_standings gs://f1-de-bucket/silver/driver_standings.parquet/*.parquet

echo "Loading drivers..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.drivers gs://f1-de-bucket/silver/drivers.parquet/*.parquet

echo "Loading lap_times..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.lap_times gs://f1-de-bucket/silver/lap_times.parquet/*.parquet

echo "Loading pit_stops..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.pit_stops gs://f1-de-bucket/silver/pit_stops.parquet/*.parquet

echo "Loading qualifying..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.qualifying gs://f1-de-bucket/silver/qualifying.parquet/*.parquet

echo "Loading races..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.races gs://f1-de-bucket/silver/races.parquet/*.parquet

echo "Loading results..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.results gs://f1-de-bucket/silver/results.parquet/*.parquet

echo "Loading seasons..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.seasons gs://f1-de-bucket/silver/seasons.parquet/*.parquet

echo "Loading sprint_results..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.sprint_results gs://f1-de-bucket/silver/sprint_results.parquet/*.parquet

echo "Loading status..."
bq load --source_format=PARQUET data-engineer-zoomcamp-448404:f1_data.status gs://f1-de-bucket/silver/status.parquet/*.parquet
