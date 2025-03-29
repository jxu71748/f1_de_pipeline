import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def download_f1_dataset(download_path="raw_data"):
    os.makedirs(download_path, exist_ok=True)

    api = KaggleApi()
    api.authenticate()
    print("Kaggle API Authenticated Successfully")

    print("Downloading dataset...")
    dataset = "rohanrao/formula-1-world-championship-1950-2020"
    api.dataset_download_files(dataset, path=download_path, quiet=False, force=True)

    zip_file = os.path.join(download_path, "formula-1-world-championship-1950-2020.zip")

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(download_path)

    os.remove(zip_file)
    print("Download complete and files extracted.")

if __name__ == "__main__":
    download_f1_dataset()
    