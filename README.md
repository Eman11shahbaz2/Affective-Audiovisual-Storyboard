# Storyboard Automator

This Python project automatically turns a written story into a narrated video storyboard. You provide the text, and the code handles the rest.

### What it does

* **Voice:** Generates professional AI voiceovers for your script using ElevenLabs.
* **Art:** Creates matching cinematic images for each scene using Pollinations AI.
* **Editing:** Automatically stitches the audio and images together, syncing everything perfectly into a final MP4 video.

### How to use it

1. **Install requirements:**
`pip install requests python-dotenv moviepy`
2. **Add your keys:** Save your ElevenLabs and Pollinations AI keys in a `.env` file.
3. **Run the code:** Run your generation scripts to download the assets, then run the stitcher to build the video.
```bash
python generate_visuals.py
python stitch_prototype.py

```
