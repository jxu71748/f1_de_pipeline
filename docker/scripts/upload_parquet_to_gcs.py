import os
from google.cloud import storage

def upload_parquet_to_gcs(bucket_name, source_folder, destination_folder="silver"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for folder in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder)
        if os.path.isdir(folder_path):  # ensure parquet output folder
            for root, _, files in os.walk(folder_path):
                for file in files:
                    local_path = os.path.join(root, file)

                    # Build the storage path in GCS (preserve directory structure)
                    relative_path = os.path.relpath(local_path, source_folder)
                    blob_path = os.path.join(destination_folder, relative_path)

                    blob = bucket.blob(blob_path)
                    if not blob.exists(client):
                        print(f"Uploading {local_path} to gs://{bucket_name}/{blob_path}")
                        blob.upload_from_filename(local_path)
                    else:
                        print(f"Skipping {relative_path}, already exists.")
    
    print("All Parquet files uploaded to GCS (silver layer) successfully")

if __name__ == "__main__":
    bucket_name = "f1-de-bucket"
    source_folder = "/opt/airflow/data/transformed"

    upload_parquet_to_gcs(bucket_name, source_folder)
