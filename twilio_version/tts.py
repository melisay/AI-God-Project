import os
import time
import hashlib
import requests
from .config import ELEVENLABS_API_KEY, current_voice, CACHE_DIR
from .cache_logging import debug_log

def generate_tts_streaming(text, filename=None):
    """
    Generates text-to-speech audio using ElevenLabs and plays it using CoreAudio.
    Ensures only one playback process is running at a time.
    """
    if not filename:
        filename = os.path.join(CACHE_DIR, f"dynamic_{hashlib.md5(text.encode()).hexdigest()}.mp3")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{current_voice}/stream?optimize_streaming_latency=3"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text,
        "voice_settings": {"stability": 0.3, "similarity_boost": 0.4}
    }

    try:
        start_time = time.time()
        response = requests.post(url, json=data, headers=headers, stream=True)
        if response.status_code == 200:
            with open(filename, "wb") as audio_file:
                for chunk in response.iter_content(chunk_size=512):
                    audio_file.write(chunk)

            latency = time.time() - start_time
            debug_log(f"TTS saved to {filename}. Latency: {latency:.2f} seconds")

            # ✅ **Kill any previous mpg123 processes before playing new audio**
            os.system("pkill -9 mpg123")

            playback_command = f"mpg123 -o coreaudio {filename}"
            debug_log(f"Playing audio: {playback_command}")
            os.system(playback_command)  # Ensure playback runs synchronously

            return filename
        else:
            debug_log(f"TTS failed with status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        debug_log(f"TTS streaming exception: {e}")
        return None
