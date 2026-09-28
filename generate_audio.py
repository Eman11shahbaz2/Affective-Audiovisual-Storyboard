import os
import json
import time
import requests
from dotenv import load_dotenv

# 1. Authenticate
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")


voice_id = "cgSgspJ2msm6clMCkdW9"
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": api_key
}

# 2. Load the mapped JSON data you created on Day 12
json_path = "outputs/suspense_payload.json"
with open(json_path, "r", encoding="utf-8") as file:
    payload = json.load(file)

print(f"\n=== Generating Audio for: {payload['project_name']} ===")

# 3. Loop through every scene in the JSON file
for scene in payload["scenes"]:
    scene_id = scene["scene_id"]
    
    # Dig into the JSON structure to grab the text and target WPM
    text = scene["api_payloads"]["audio_api"]["text_to_speak"]
    target_wpm = scene["api_payloads"]["audio_api"]["target_wpm"]
    
    print(f"Processing Scene {scene_id}... (Target: {target_wpm} WPM)")
    
    # 4. Prepare the exact payload for ElevenLabs
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    # 5. Send the request
    response = requests.post(url, json=data, headers=headers)
    
    # 6. Save the file dynamically using the scene ID
    if response.status_code == 200:
        output_file = f"outputs/scene_{scene_id}.mp3"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f" -> Saved: {output_file}")
    else:
        print(f" -> Failed on Scene {scene_id}: {response.status_code}")
        print(response.text)
        
    # Pause for 1 second between requests to avoid hitting free-tier API rate limits
    time.sleep(1)
    
print("\nAll audio generated successfully!")