import os
from google.cloud import storage
from google.oauth2 import service_account

def upload_files_to_gcs(bucket_name, source_folder, destination_folder="raw"):
    credentials_path = "/opt/airflow/credentials/google_credentials.json"
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)

    for filename in os.listdir(source_folder):
        if filename.endswith(".csv"):
            local_path = os.path.join(source_folder, filename)
            blob_path = f"{destination_folder}/{filename}"
            blob = bucket.blob(blob_path)

            if not blob.exists(client):
                print(f"Uploading {local_path} to gs://{bucket_name}/{blob_path}...")
                blob.upload_from_filename(local_path)
            else:
                print(f"Skipping {filename}, already exists in GCS.")
    
    print("All files uploaded to GCS successfully.")

if __name__ == "__main__":
    bucket_name = "f1-de-bucket"
    source_folder = "/opt/airflow/raw_data"

    upload_files_to_gcs(bucket_name, source_folder)
