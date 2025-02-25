import os
import time
import json
import pyaudio
import speech_recognition as sr
from vosk import KaldiRecognizer
from .config import VOSK_MODEL
from .logging import debug_log
import subprocess  # Add this import
import wave  # Add this import
import hashlib  # Add this import

CACHE_DIR = "/path/to/cache"  # Define CACHE_DIR

def listen_to_user(audio_file="temp.wav"):
    """
    Captures audio input and processes it using Vosk.
    Args:
        audio_file (str): The file path to save temporary audio.
    Returns:
        str: The recognized text, or an empty string if recognition fails.
    """
    try:
        # Record audio using arecord (or similar tool)
        subprocess.run(
            ["arecord", "-D", "plughw:1,0", "-f", "S16_LE", "-r", "16000", "-d", "4", "-q", audio_file],
            check=True
        )

        # Process the recorded audio
        with wave.open(audio_file, "rb") as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                raise ValueError("Audio file must be mono, 16-bit, with a 16kHz sample rate.")

            recognizer = KaldiRecognizer(VOSK_MODEL, wf.getframerate())
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    return result.get("text", "").strip()

        return ""
    except Exception as e:
        debug_log(f"Error during Vosk recognition: {e}")
        return ""

def process_user_input(user_input):
    """
    Processes user input, fetches AI response, and generates TTS.
    Logs structured debugging output including latencies.
    """
    total_start = time.time()

    # Generate cache key
    cache_key = hashlib.md5(user_input.encode()).hexdigest()
    cached_file = os.path.join(CACHE_DIR, f"cached_{cache_key}.mp3")

    # Check if response is already cached
    if os.path.exists(cached_file):
        debug_log(
            "Using cached response for user input.",
            structured_data={
                "User Said": user_input,
                "Cached File": cached_file,
            },
        )
        return cached_file

    # Fetch AI response
    chatgpt_start = time.time()
    ai_response = get_chatgpt_response(user_input)
    chatgpt_latency = time.time() - chatgpt_start

    # Generate TTS
    tts_start = time.time()
    tts_file = generate_tts_streaming(ai_response, cached_file)
    tts_latency = time.time() - tts_start

    # Log structured debugging information with full details
    total_latency = time.time() - total_start
    debug_log(
        "Processed user input with detailed latencies.",
        structured_data={
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Message": "Processed user input with detailed latencies.",
            "User Said": user_input,
            "GOD Said": ai_response,
            "Cached File": cached_file,
            "Latencies": {
                "ChatGPT Latency (s)": round(chatgpt_latency, 2),
                "TTS Latency (s)": round(tts_latency, 2),
                "Total Processing Latency (s)": round(total_latency, 2),
            },
        },
    )

    return tts_file

def get_chatgpt_response(user_input):
    """
    Mock function to simulate fetching a response from ChatGPT.
    Replace this with actual implementation.
    """
    return "This is a mock response from ChatGPT."

def generate_tts_streaming(ai_response, cached_file):
    """
    Mock function to simulate TTS generation.
    Replace this with actual implementation.
    """
    with open(cached_file, 'w') as f:
        f.write("This is a mock TTS file.")
    return cached_file