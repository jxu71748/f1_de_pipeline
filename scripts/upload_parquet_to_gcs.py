import os
from google.cloud import storage

def upload_parquet_files(bucket_name, source_folder, destination_folder="silver"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for filename in os.listdir(source_folder):
        if filename.endswith(".parquet"):
            local_path = os.path.join(source_folder, filename)
            blob_path = f"{destination_folder}/{filename}"
            blob = bucket.blob(blob_path)

            if not blob.exists(client):
                print(f"Uploading {local_path} to gs://{bucket_name}/{blob_path}...")
                blob.upload_from_filename(local_path)
            else:
                print(f"Skipping {filename}, already exists in GCS.")

    print("All Parquet files uploaded to GCS successfully.")

if __name__ == "__main__":
    BUCKET_NAME = "f1-de-bucket"
    SOURCE_FOLDER = "data/transformed"
    upload_parquet_files(BUCKET_NAME, SOURCE_FOLDER)
