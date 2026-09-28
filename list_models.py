import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("VIDEO_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("Fetching available models from Google...\n")
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get("models", [])
    for model in models:
        # We only want to print models that start with 'veo' or handle video
        name = model.get("name", "")
        if "veo" in name.lower() or "video" in name.lower():
            print(f"Found model: {name}")
else:
    print(f"Error {response.status_code}: {response.text}")