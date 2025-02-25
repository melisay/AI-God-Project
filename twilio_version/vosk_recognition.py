import os
import wave
import json
import subprocess
from vosk import Model, KaldiRecognizer
from .cache_logging import debug_log

# Constants
BASE_DIR = "/Users/nipsvanmctitsky/phonegod"
VOSK_MODEL_PATH = os.path.expanduser(f"{BASE_DIR}/vosk_models/vosk-model-small-en-us-0.15")

# Load Vosk model
try:
    VOSK_MODEL = Model(VOSK_MODEL_PATH)
    print("Vosk model loaded successfully.")
except Exception as e:
    print(f"Failed to load Vosk model: {e}")

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
