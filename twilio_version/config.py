import os
from dotenv import load_dotenv
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Constants
BASE_DIR = "/Users/nipsvanmctitsky/phonegod"
CONVERSATION_LOG_FILE = "conversation_log.json"
RESPONSE_FILE = f"{BASE_DIR}/static/response.mp3"
FALLBACK_FILE = f"{BASE_DIR}/static/fallback.mp3"
WELCOME_FILE = f"{BASE_DIR}/static/welcome.mp3"
CACHE_DIR = f"{BASE_DIR}/static/cached_responses"
VOSK_MODEL_PATH = os.path.expanduser(f"{BASE_DIR}/vosk_models/vosk-model-small-en-us-0.15")

# Ensure directories exist
os.makedirs(CACHE_DIR, exist_ok=True)
if not os.path.exists(VOSK_MODEL_PATH):
    raise FileNotFoundError(f"Vosk model not found at {VOSK_MODEL_PATH}")

# Load Vosk model
try:
    from vosk import Model
    VOSK_MODEL = Model(VOSK_MODEL_PATH)
    print("Vosk model loaded successfully.")
except Exception as e:
    print(f"Failed to load Vosk model: {e}")

# API keys
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check API keys
if not ELEVENLABS_API_KEY:
    raise ValueError("Missing ELEVENLABS_API_KEY environment variable.")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY environment variable.")

# ElevenLabs TTS settings
import elevenlabs
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
LOG_FILE = "/Users/nipsvanmctitsky/phonegod/local_debug.log"

idle_mode = threading.Event()
stop_playback = threading.Event()
cache_lock = threading.Lock()

# Add a global dictionary for caching
chatgpt_cache = {}
PRELOADED_RESPONSES = {}

# Use ThreadPoolExecutor for parallel execution
executor = ThreadPoolExecutor(max_workers=4)

# Flask app setup
app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
)