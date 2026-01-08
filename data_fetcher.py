import pandas as pd
import requests
import os
from tqdm import tqdm
import shutil  # Added for zipping
import time

# --- CONFIGURATION ---
MAPBOX_TOKEN = "pk.eyJ1IjoibWFoaXBhbDAxIiwiYSI6ImNtamViN2hncDBnN3czY3M4a3F4MHFxb3cifQ.p_15yvzvrw0qlhcw0S_4qg"

# Image Settings
ZOOM_LEVEL = 18       
IMAGE_SIZE = "224x224" 
STYLE_ID = "mapbox/satellite-v9"

# --- PATHS (Updated for Local Machine) ---
# Assumes the excel file is in the same directory as this script
DATASET_FILENAME = "train(1).xlsx" 
DATASET_PATH = os.path.join(os.getcwd(), DATASET_FILENAME)

# Folder to store images temporarily
OUTPUT_DIR = os.path.join(os.getcwd(), "satellite_images_temp") 

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_mapbox_image(lat, long, image_id):
    """
    Fetches a static satellite image from Mapbox.
    NOTE: Mapbox requires coordinates in (Longitude, Latitude) format.
    """
    save_path = os.path.join(OUTPUT_DIR, f"{image_id}.jpg")
    
    # Check if image already exists to save API credits and time
    if os.path.exists(save_path):
        return "Exists"

    # URL construction
    url = f"https://api.mapbox.com/styles/v1/{STYLE_ID}/static/{long},{lat},{ZOOM_LEVEL},0/{IMAGE_SIZE}?access_token={MAPBOX_TOKEN}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return "Downloaded"
        else:
            print(f"Failed ID {image_id}: {response.status_code} - {response.text}")
            return "Error"
    except Exception as e:
        print(f"Exception for ID {image_id}: {e}")
        return "Error"

def run_downloader():
    # 1. Load Dataset
    if not os.path.exists(DATASET_PATH):
        print(f"Error: Could not find {DATASET_FILENAME} in the current directory.")
        print(f"Looking in: {DATASET_PATH}")
        return

    print("Loading dataset...")
    if DATASET_PATH.endswith('.xlsx'):
        df = pd.read_excel(DATASET_PATH)
    else:
        df = pd.read_csv(DATASET_PATH)

    print(f"Found {len(df)} properties. Starting download...")
    
    # 2. Download Images
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        # Ensure column names match your Excel file (lat, long, id)
        fetch_mapbox_image(row['lat'], row['long'], row['id'])

    print("Download complete!")
    
    # 3. Zip the Folder
    print("Zipping images into 'satellite_images.zip'...")
    
    # The first argument is the name of the zip file (without extension)
    # The second is the format ('zip')
    # The third is the folder to zip
    shutil.make_archive("satellite_images", 'zip', OUTPUT_DIR)
    
    print(f"Success! Created satellite_images.zip in {os.getcwd()}")
    
    # Optional: Clean up the temp folder to save space
    # shutil.rmtree(OUTPUT_DIR) 

if __name__ == "__main__":
    run_downloader()