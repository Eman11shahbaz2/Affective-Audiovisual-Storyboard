import json
import os
# Import directly from moviepy instead of moviepy.editor
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

with open("outputs/suspense_payload.json", "r", encoding="utf-8") as file:
    payload = json.load(file)

print(f"\n=== Stitching Final Prototype: {payload['project_name']} ===")

video_clips = []

for scene in payload["scenes"]:
    scene_id = scene["scene_id"]
    image_path = f"outputs/scene_{scene_id}.png"
    audio_path = f"outputs/scene_{scene_id}.mp3"
    
    if os.path.exists(image_path) and os.path.exists(audio_path):
        print(f"Processing Scene {scene_id}...")
        
        audio_clip = AudioFileClip(audio_path)
        
        # Use v2.0 methods: with_duration and with_audio
        image_clip = ImageClip(image_path).with_duration(audio_clip.duration)
        video_clip = image_clip.with_audio(audio_clip)
        
        video_clips.append(video_clip)
    else:
        print(f"Skipping Scene {scene_id} - Missing image or audio file.")

if video_clips:
    print("\nStitching all scenes together... (This will take a minute to encode)")
    
    # Removed method="compose" to prevent audio track dropping
    final_video = concatenate_videoclips(video_clips)
    
    output_path = "outputs/final_storyboard.mp4"
    final_video.write_videofile(
        output_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="libmp3lame" # Changed to a universally supported mp3 codec
    )
    
    print(f"\nSuccess! Prototype saved to {output_path}")
else:
    print("\nError: No valid scenes found to stitch.")