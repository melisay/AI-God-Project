import os
import threading
from dotenv import load_dotenv
from vosk import Model, KaldiRecognizer
from concurrent.futures import ThreadPoolExecutor
import openai
import elevenlabs

# Constants
BASE_DIR = "/Users/nipsvanmctitsky/AI-God-Project/"
CONVERSATION_LOG_FILE = os.path.join(BASE_DIR, "conversation_log.json")
RESPONSE_FILE = os.path.join(BASE_DIR, "static", "response.mp3")
FALLBACK_FILE = os.path.join(BASE_DIR, "static", "fallback.mp3")
WELCOME_FILE = os.path.join(BASE_DIR, "static", "welcome.mp3")
CACHE_DIR = os.path.join(BASE_DIR, "static", "cached_responses")
VOSK_MODEL_PATH = os.path.expanduser(os.path.join(BASE_DIR, "vosk_models", "vosk-model-small-en-us-0.15"))
LOG_FILE = os.path.join(BASE_DIR, "local_version", "local_debug.log")

# Ensure directories exist
for directory in [CACHE_DIR, os.path.dirname(LOG_FILE)]:
    os.makedirs(directory, exist_ok=True)

# Load Vosk model
if os.path.exists(VOSK_MODEL_PATH):
    try:
        VOSK_MODEL = Model(VOSK_MODEL_PATH)
        print("Vosk model loaded successfully.")
    except Exception as e:
        print(f"Failed to load Vosk model: {e}")
else:
    print(f"WARNING: Vosk model not found at {VOSK_MODEL_PATH}. Check installation.")

# Load environment variables
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check API keys
if not ELEVENLABS_API_KEY:
    raise ValueError("Missing ELEVENLABS_API_KEY environment variable.")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable.")

# ElevenLabs TTS settings
client = elevenlabs.ElevenLabs(api_key=ELEVENLABS_API_KEY)
VOICE_NIKKI = "WoGJO0bsQ5xvIQwKIRtC"
VOICE_TOM = "OWXgblXycW2yI83Vj3xf"
current_voice = VOICE_NIKKI

# Global state
WAKE_UP_WORDS = ["are you there", "wake up", "hello god"]
INTERRUPT_KEYWORDS = ["stop", "enough", "next", "shut your face"]
DYNAMIC_KEYWORDS = ["new", "another", "different", "something else"]
IDLE_TIMEOUT = 30  # Time in seconds before idle mode is triggered
SLEEP_INTERVAL = 30  # Time in seconds to wait between idle retries

MAX_CACHE_SIZE = 100  # Limit to 100 items

DEBUG = True

idle_mode = threading.Event()
stop_playback = threading.Event()
cache_lock = threading.Lock()
exit_program = threading.Event()

# Add a global dictionary for caching
chatgpt_cache = {}
PRELOADED_RESPONSES = {}

# Use ThreadPoolExecutor for parallel execution
executor = ThreadPoolExecutor(max_workers=4)

# Function to check if input is a wake-up word
def is_wake_up_word(user_input):
    keywords_only = set(WAKE_UP_WORDS) - {"what's the airspeed velocity of an unladen swallow", "can you hear me"}
    return any(keyword in user_input for keyword in keywords_only)

# Function to cache AI responses
def set_cache(key, value):
    with cache_lock:
        chatgpt_cache[key] = value
