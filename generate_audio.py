import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from stories import STORIES

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("SARVAM_API_KEY")

if not API_KEY:
    raise ValueError("SARVAM_API_KEY not found. Please add it to your .env file.")

API_URL = "https://api.sarvam.ai/text-to-speech/stream"

# Ensure audio/ directory exists
Path("audio").mkdir(exist_ok=True)


def generate_audio(story: dict):
    print(f"\n🎙️  Generating audio for: {story['title']} ({story['title_english']})")

    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": story["text"],
        "target_language_code": "te-IN",
        "speaker": "ishita",
        "model": "bulbul:v3",
        "pace": 0.85,
        "speech_sample_rate": 22050,
        "output_audio_codec": "mp3",
        "enable_preprocessing": True
    }

    output_path = Path("audio") / story["filename"]

    with requests.post(API_URL, headers=headers, json=payload, stream=True) as response:
        response.raise_for_status()

        total_bytes = 0
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    total_bytes += len(chunk)
                    print(f"  ↳ Received {total_bytes} bytes...", end="\r")

    print(f"\n  ✅ Saved to {output_path}  ({total_bytes / 1024:.1f} KB)")


if __name__ == "__main__":
    print("=" * 50)
    print("  Telugu TTS — Sarvam AI (Ishita / bulbul:v3)")
    print("=" * 50)

    for story in STORIES:
        generate_audio(story)

    print("\n🎉 All stories generated successfully!")
    print("📁 Find your MP3 files in the audio/ folder.")
