import os
import urllib.request
import zipfile

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip"
MODEL_DIR = "model"
ZIP_NAME = "vosk-model-small-hi-0.22.zip"

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

zip_path = os.path.join(MODEL_DIR, ZIP_NAME)

print("Downloading Vosk model...")
urllib.request.urlretrieve(MODEL_URL, zip_path)

print("Unzipping model...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(MODEL_DIR)

print("Cleaning up zip file...")
os.remove(zip_path)

print("Model ready in:", os.path.join(MODEL_DIR, "vosk-model-small-hi-0.22"))
