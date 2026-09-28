import json
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from config import MAPPING_RULES 

# Ensure required NLTK resources are downloaded
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('vader_lexicon', quiet=True)

analyzer = SentimentIntensityAnalyzer()
file_path = "test_scripts/suspense.txt"

with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

sentences = nltk.sent_tokenize(raw_text)

# 1. Create the empty master template based on Day 5 schema
final_output = {
    "project_name": "Suspense_Test",
    "scenes": []
}

print(f"Processing '{file_path}' into JSON...")

for scene_number, sentence in enumerate(sentences, start=1):
    
    scores = analyzer.polarity_scores(sentence)
    valence = scores['compound']
    
    words = nltk.word_tokenize(sentence)
    is_high_arousal = len(words) < 8 or "!" in sentence
    
    if valence <= -0.1:
        mapped_emotion = "suspense" if is_high_arousal else "melancholy"
    elif valence >= 0.1:
        mapped_emotion = "joy" if is_high_arousal else "calm"
    else:
        mapped_emotion = "neutral"
        
    pacing_data = MAPPING_RULES[mapped_emotion]
    
    # 2. Package this specific scene's data into a dictionary
    scene_data = {
        "scene_id": scene_number,
        "raw_text": sentence,
        "cognitive_analysis": {
            "valence_score": valence,
            "arousal_indicator": "High" if is_high_arousal else "Low",
            "mapped_emotion": mapped_emotion
        },
        "api_payloads": {
            "audio_api": {
                "text_to_speak": sentence,
                "target_wpm": pacing_data['wpm']
            },
            "video_api": {
                "duration_seconds": pacing_data['video_duration_seconds'],
                # Combine the sentence with the visual style rules
                "generation_prompt": f"{sentence} {pacing_data['visual_style']}" 
            }
        }
    }
    
    # 3. Add this scene to our master template's 'scenes' list
    final_output["scenes"].append(scene_data)

# 4. Create an 'outputs' folder if it doesn't exist yet
os.makedirs("outputs", exist_ok=True)

# 5. Save the master template as an actual .json file
output_filename = "outputs/suspense_payload.json"
with open(output_filename, "w", encoding="utf-8") as json_file:
    json.dump(final_output, json_file, indent=2)

print(f"Success! Data mapped and saved to {output_filename}")