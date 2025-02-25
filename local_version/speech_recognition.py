import os
import time
import json
import pyaudio
import speech_recognition as sr
from vosk import KaldiRecognizer
from .config import VOSK_MODEL, idle_mode, stop_playback, exit_program
from .logging import debug_log

# Add missing imports and variables
import hashlib
from .config import CACHE_DIR, INTERRUPT_KEYWORDS
from .tts import generate_tts_streaming, get_chatgpt_response

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

# Updated: interruption
def listen_for_interruptions():
    """
    Continuously listens for interruption keywords during AI playback.
    Pauses playback and transitions back to the conversational flow seamlessly.
    """
    global stop_playback
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            while not exit_program.is_set():
                # audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                user_input = recognizer.recognize_google(audio).lower()
                if any(keyword in user_input for keyword in INTERRUPT_KEYWORDS):
                    debug_log(f"Interruption detected: '{user_input}'")
                    stop_playback.set()
                    
                    # Clear current playback and TTS
                    os.system("pkill mpg123")
                    generate_tts_streaming("Alright, stopping. What's on your mind?")
                    
                    # Listen for new input
                    new_input = listen_to_user().strip().lower()
                    if new_input:
                        debug_log(f"Processing user input after interruption: '{new_input}'")
                        response = get_chatgpt_response(new_input)
                        generate_tts_streaming(response)
                    break
        except sr.WaitTimeoutError:
            debug_log("No interruption detected: Timeout.")
        except sr.UnknownValueError:
            debug_log("Interruption error: Unrecognizable input.")
        except Exception as e:
            debug_log(f"Error while listening for interruptions: {e}")
            
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
        debug_log("Using cached response.", {"User Said": user_input, "Cached File": cached_file})
        return cached_file

    # Fetch AI response
    chatgpt_start = time.time()
    ai_response = get_chatgpt_response(user_input)
    chatgpt_latency = time.time() - chatgpt_start

    # Generate TTS
    tts_start = time.time()
    cached_file = generate_tts_streaming(ai_response, cached_file)
    tts_latency = time.time() - tts_start

    # Return the generated file instead of playing it again**
    total_latency = time.time() - total_start
    debug_log("Processed user input with detailed latencies.", {
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "User Said": user_input,
        "GOD Said": ai_response,
        "Cached File": cached_file,
        "Latencies": {
            "ChatGPT Latency (s)": round(chatgpt_latency, 2),
            "TTS Latency (s)": round(tts_latency, 2),
            "Total Processing Latency (s)": round(total_latency, 2),
        },
    })

    return cached_file  # Ensure playback is handled only once
