import os
from google.cloud import storage

def upload_files_to_gcs(bucket_name, source_folder, destination_folder="raw"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    for filename in os.listdir(source_folder):
        if filename.endswith(".csv"):
            local_path = os.path.join(source_folder, filename)
            blob_path = f"{destination_folder}/{filename}"
            blob = bucket.blob(blob_path)

            print(f"Uploading {local_path} to gs://{bucket_name}/{blob_path}...")
            blob.upload_from_filename(local_path)
    
    print("All files uploaded to GCS successfully.")

if __name__ == "__main__":
    bucket_name = "f1-de-bucket"
    source_folder = "raw_data"

    upload_files_to_gcs(bucket_name, source_folder)
