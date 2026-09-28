import os
import requests
from dotenv import load_dotenv

# 1. Open the vault: Load the secret key from your .env file
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

if not api_key:
    print("Error: Could not find ELEVENLABS_API_KEY. Check your .env file.")
    exit()

# 2. Set up the ElevenLabs API request
# '21m00Tcm4TlvDq8ikWAM' is the default Voice ID for a voice named "Rachel"
voice_id = "cgSgspJ2msm6clMCkdW9"
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

# These headers act as your digital ID badge to prove you are allowed to make this request
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": api_key
}

# 3. Define the hard-coded test payload
data = {
    "text": "Hello! This is a test of the Eleven Labs API integration.",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}

print("Sending request to ElevenLabs... (this might take a few seconds)")

# 4. Make the HTTP POST request to the API
response = requests.post(url, json=data, headers=headers)

# 5. Check the result and save the audio file
if response.status_code == 200:
    os.makedirs("outputs", exist_ok=True)
    output_file = "outputs/day16_test.mp3"
    
    # 'wb' means Write Binary (used for saving media files like audio/video)
    with open(output_file, "wb") as file:
        file.write(response.content)
        
    print(f"Success! Audio saved to {output_file}")
else:
    print(f"Failed! API returned an error: {response.status_code}")
    print(response.text)