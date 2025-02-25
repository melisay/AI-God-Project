import os
import time
import hashlib
import requests
from .config import ELEVENLABS_API_KEY, current_voice, CACHE_DIR
from .logging import debug_log
from .config import openai, cache_lock, chatgpt_cache, set_cache


MAX_CACHE_SIZE = 100  # Limit to 100 items

def set_cache(key, value):
    """
    Sets a value in the cache, respecting the cache size limit.
    """
    with cache_lock:
        if len(chatgpt_cache) >= MAX_CACHE_SIZE:
            # Remove the oldest item (FIFO eviction)
            chatgpt_cache.pop(next(iter(chatgpt_cache)))
        chatgpt_cache[key] = value
        
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

# Personality prompt
current_mode = "john_oliver"
personality_prompts = {
    "john_oliver": (
        "You are a sarcastic and humorous version of God. Always respond with very short, witty, and punchy one-liners. "
        "No more than 10 words, prioritizing sarcasm and humor over depth."
    )
}


def get_chatgpt_response(prompt, dynamic=False):
    """
    Fetches a response from ChatGPT.
    Args:
        prompt (str): The user's input.
        dynamic (bool): If True, generates a new response regardless of cache.
    Returns:
        str: The AI's response.
    """
    cache_key = hashlib.md5(prompt.encode()).hexdigest()

    # If not dynamic and response is cached, return the cached response
    if not dynamic and cache_key in chatgpt_cache:
        debug_log(f"Cache hit for prompt: {prompt}")
        return chatgpt_cache[cache_key]

    try:
        start_time = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": personality_prompts.get("john_oliver", "You are an AI.")},
                {"role": "user", "content": prompt[:100]}  # Truncate prompt for brevity
            ],
            max_tokens=25,
            temperature=0.7
        )
        latency = time.time() - start_time
        debug_log(f"ChatGPT response latency: {latency:.2f} seconds")

        # Extract the response
        ai_response = response["choices"][0]["message"]["content"]

        # Cache response only for non-dynamic prompts
        if not dynamic:
            set_cache(cache_key, ai_response)

        return ai_response
    except Exception as e:
        debug_log(f"Error fetching ChatGPT response: {e}")
        return "I'm having trouble connecting to divine wisdom right now."