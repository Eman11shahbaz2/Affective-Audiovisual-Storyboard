import os
import json
import urllib.parse
import requests
import time
from dotenv import load_dotenv

# 1. Load the free key from your environment
load_dotenv()
api_key = os.getenv("POLLINATIONS_KEY")

with open("outputs/suspense_payload.json", "r", encoding="utf-8") as file:
    payload = json.load(file)

print(f"\n=== Generating Free Storyboard Images for: {payload['project_name']} ===")
os.makedirs("outputs", exist_ok=True)

for scene in payload["scenes"]:
    scene_id = scene["scene_id"]
    prompt = scene["api_payloads"]["video_api"]["generation_prompt"]
    
    print(f"Generating Scene {scene_id} image...")
    safe_prompt = urllib.parse.quote(prompt)
    
    # 2. Pass the key in the URL string
    url = f"https://gen.pollinations.ai/image/{safe_prompt}?width=1920&height=1080&nologo=true&key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        output_file = f"outputs/scene_{scene_id}.png"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f" -> Success! Saved {output_file}")
    else:
        print(f" -> Failed to generate Scene {scene_id}: {response.status_code}")
        print(response.text)
        
    time.sleep(2)
    
print("\nAll storyboard keyframes generated!")