## tts.py
import requests
import os
from config.config import ELEVENLABS_API_KEY, CACHE_DIR, current_voice

def generate_tts(text, filename):
    """ Generates speech using ElevenLabs and saves to a file """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{current_voice}/stream?optimize_streaming_latency=3"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text, "voice_settings": {"stability": 0.3, "similarity_boost": 0.5}}
    
    response = requests.post(url, json=data, headers=headers, stream=True)
    if response.status_code == 200:
        filepath = os.path.join(CACHE_DIR, filename)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=512):
                f.write(chunk)
        return filepath
    else:
        print(f"Error generating TTS: {response.text}")
        return None