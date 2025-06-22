import requests
import os

def download_csv(filename="Electric_Vehicle_Population_Data.csv"):

    base_dir = "/opt/airflow/data"
    os.makedirs(base_dir, exist_ok=True)

    path = os.path.join(base_dir, filename)

    url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded CSV to {path}")
    else:
        raise Exception(f"Failed to download: {response.status_code}")
