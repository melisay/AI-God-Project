import os
import time
import json
import pyaudio
import speech_recognition as sr
from vosk import KaldiRecognizer
from .config import VOSK_MODEL
from .logging import debug_log

def listen_to_user():
    """Listen for user input using the Vosk model with the correct microphone device."""
    p = pyaudio.PyAudio()
    valid_devices = []

    # List available audio devices
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        debug_log(f"Device {i}: {info['name']} (Input Channels: {info['maxInputChannels']})")
        if info["maxInputChannels"] > 0:  # Only consider devices with input channels
            valid_devices.append(i)

    p.terminate()

    if not valid_devices:
        debug_log("No valid input devices found!")
        return "", 0.0

    # Automatically select the first valid input device
    device_index = valid_devices[0]  # Use the first valid microphone

    recognizer = KaldiRecognizer(VOSK_MODEL, 16000)
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=2000,
        input_device_index=device_index
    )
    stream.start_stream()

    debug_log(f"Listening for user input on device {device_index}.")

    start_time = time.time()

    try:
        while True:
            data = stream.read(2000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                latency = time.time() - start_time
                text = json.loads(result).get("text", "").lower()
                debug_log(f"Recognized text: {text}")
                return text, latency
    except Exception as e:
        debug_log(f"Error during speech recognition: {e}")
        return "", 0.0
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
