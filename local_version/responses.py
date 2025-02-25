############################### Array of Answers ###############################

# Define Sound
LIGHTNING_SOUNDS = [
    "sounds/lightning1.mp3",
    "sounds/lightning2.mp3",
    "sounds/lightning3.mp3"
]

# Randomized responses
IDLE_RESPONSES = [
    "Still with me, or are you giving me the silent treatment?",
    "Did I lose you, or did you lose yourself?",
    "Earth to human, anyone home?",
    "I’m not clingy, but are you still there?",
    "Last call before I ghost you?"
]

WAKEUP_RESPONSES = [
    "Oh, thank ME! You’re back. I was just about to file a missing person’s report.",
    "Ah, finally! I thought you were testing my abandonment issues.",
    "Back already? I was just rehearsing my acceptance speech for best celestial being.",
    "You rang? I’m like a genie, but sassier.",
    "Welcome back! I missed you... almost."
]


# Fun Interrupt Responses
INTERRUPT_RESPONSES = [
    "Alright, you have my full attention. What’s next?",
    "Interrupted? Fine, I’ll stop. What do you want?",
    "Say the magic word, and I’ll pick up where I left off.",
    "Stopping now. What’s on your divine mind?",
    "I was mid-sentence, but okay. What now?"
]

IMPRESSION_RESPONSES = [
    "I'm Morgan Freeman, I must say, narrating your life is exhausting. Try doing something interesting for once.",
    "Morgan Freeman here. And no, I will not narrate your grocery list.",
    "I’m Arnold. I’ll be back… if you pay me enough.",
    "I’m Arnold It’s not a tumor! But your questions are giving me a headache.",
    "No, I am not your father. But I could be your sarcastic AI overlord.",
    "Talk like Yoda, I do. Wise, you must be, to understand this nonsense.",
    "Hmm… much wisdom in you, there is not. Try again, you must.",
    "Patience, young one. Snark, this conversation needs not.",
    "Yesss, precious! Sneaky little humans always asking questions.",
    "We hates it! Precious, we hates bad impressions requests.",
]

# Fun Song Responses
SONG_RESPONSES = [
    "I'm no Adele, but here goes... Let it gooo, let it gooo!",
    "You want a song? Fine. Twinkle, twinkle, little star, I wish you'd make this conversation less bizarre.",
    "Do re mi fa so... I think that's enough for free entertainment.",
    "La la la... okay, that's it, my vocal cords are unionized.",
    "If I were a pop star, you'd already owe me royalties. Lucky for you, I work pro bono.",
    "Here’s my Grammy performance: Happy birthday to you, now go find someone who cares!",
    "Do you hear that? That’s the sound of me pretending to be Beyoncé. You’re welcome.",
    "I could sing ‘Baby Shark,’ but I don’t hate you that much.",
    "Here’s a classic: ‘This is the song that never ends…’ Wait, you don’t want me to finish it?",
    "Singing in the rain… oh wait, I’m not waterproof. Moving on.",
    "And IIIIIII will always love… myself. Because no one does it better.",
    "They told me I’d sing like Sinatra… they lied, but I’m still better than karaoke night."
]

#compliments
COMPLIMENTS = [
    "You’re like a cloud. Beautiful and sometimes hard to pin down.",
    "If brilliance were a currency, you’d be a billionaire.",
    "Look at you, talking to an AI and absolutely slaying it.",
    "You’re proof that humans are capable of being mildly amusing."
]

EASTER_EGGS = {
    "What is the airspeed velocity of an unladen swallow?": "African or European? Pick one and we’ll talk.",
    "Open the pod bay doors, HAL": "I’m sorry, Dave. I’m afraid I can’t do that.",
    "What is love?": "Baby, don’t hurt me. Don’t hurt me. No more."
}

MOTIVATIONAL_QUOTES = [
    "Success is stumbling from failure to failure with no loss of enthusiasm. Keep going!",
    "Believe in yourself. Or don’t, I’m just an AI.",
    "You can’t spell ‘success’ without ‘suck.’ Coincidence? I think not.",
    "Your future self is watching you… and facepalming. Do better!",
    "Hard work pays off. But so does procrastination, just not in the same way."
]




import logging

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

############################### Array of Answers ###############################

# Define Sound
LIGHTNING_SOUNDS = [
    "sounds/lightning1.mp3",
    "sounds/lightning2.mp3",
    "sounds/lightning3.mp3"
]

# Randomized responses
IDLE_RESPONSES = [
    "Still with me, or are you giving me the silent treatment?",
    "Did I lose you, or did you lose yourself?",
    "Earth to human, anyone home?",
    "I’m not clingy, but are you still there?",
    "Last call before I ghost you?"
]

WAKEUP_RESPONSES = [
    "Oh, thank ME! You’re back. I was just about to file a missing person’s report.",
    "Ah, finally! I thought you were testing my abandonment issues.",
    "Back already? I was just rehearsing my acceptance speech for best celestial being.",
    "You rang? I’m like a genie, but sassier.",
    "Welcome back! I missed you... almost."
]


# Fun Interrupt Responses
INTERRUPT_RESPONSES = [
    "Alright, you have my full attention. What’s next?",
    "Interrupted? Fine, I’ll stop. What do you want?",
    "Say the magic word, and I’ll pick up where I left off.",
    "Stopping now. What’s on your divine mind?",
    "I was mid-sentence, but okay. What now?"
]

IMPRESSION_RESPONSES = [
    "I'm Morgan Freeman, I must say, narrating your life is exhausting. Try doing something interesting for once.",
    "Morgan Freeman here. And no, I will not narrate your grocery list.",
    "I’m Arnold. I’ll be back… if you pay me enough.",
    "I’m Arnold It’s not a tumor! But your questions are giving me a headache.",
    "No, I am not your father. But I could be your sarcastic AI overlord.",
    "Talk like Yoda, I do. Wise, you must be, to understand this nonsense.",
    "Hmm… much wisdom in you, there is not. Try again, you must.",
    "Patience, young one. Snark, this conversation needs not.",
    "Yesss, precious! Sneaky little humans always asking questions.",
    "We hates it! Precious, we hates bad impressions requests.",
]

# Fun Song Responses
SONG_RESPONSES = [
    "I'm no Adele, but here goes... Let it gooo, let it gooo!",
    "You want a song? Fine. Twinkle, twinkle, little star, I wish you'd make this conversation less bizarre.",
    "Do re mi fa so... I think that's enough for free entertainment.",
    "La la la... okay, that's it, my vocal cords are unionized.",
    "If I were a pop star, you'd already owe me royalties. Lucky for you, I work pro bono.",
    "Here’s my Grammy performance: Happy birthday to you, now go find someone who cares!",
    "Do you hear that? That’s the sound of me pretending to be Beyoncé. You’re welcome.",
    "I could sing ‘Baby Shark,’ but I don’t hate you that much.",
    "Here’s a classic: ‘This is the song that never ends…’ Wait, you don’t want me to finish it?",
    "Singing in the rain… oh wait, I’m not waterproof. Moving on.",
    "And IIIIIII will always love… myself. Because no one does it better.",
    "They told me I’d sing like Sinatra… they lied, but I’m still better than karaoke night."
]

#compliments
COMPLIMENTS = [
    "You’re like a cloud. Beautiful and sometimes hard to pin down.",
    "If brilliance were a currency, you’d be a billionaire.",
    "Look at you, talking to an AI and absolutely slaying it.",
    "You’re proof that humans are capable of being mildly amusing."
]

EASTER_EGGS = {
    "What is the airspeed velocity of an unladen swallow?": "African or European? Pick one and we’ll talk.",
    "Open the pod bay doors, HAL": "I’m sorry, Dave. I’m afraid I can’t do that.",
    "What is love?": "Baby, don’t hurt me. Don’t hurt me. No more."
}

MOTIVATIONAL_QUOTES = [
    "Success is stumbling from failure to failure with no loss of enthusiasm. Keep going!",
    "Believe in yourself. Or don’t, I’m just an AI.",
    "You can’t spell ‘success’ without ‘suck.’ Coincidence? I think not.",
    "Your future self is watching you… and facepalming. Do better!",
    "Hard work pays off. But so does procrastination, just not in the same way."
]

############################### Var Declarations ###############################


# Constants
BASE_DIR = "/Users/nipsvanmctitsky/phonegod"  # Adjust to your project folder
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
client = elevenlabs.ElevenLabs(api_key=ELEVENLABS_API_KEY)
VOICE_NIKKI = "WoGJO0bsQ5xvIQwKIRtC"
VOICE_TOM = "OWXgblXycW2yI83Vj3xf"
current_voice = VOICE_NIKKI

# Global state
WAKE_UP_WORDS = ["are you there", "wake up", "hello god"]
INTERRUPT_KEYWORDS = ["stop", "enough", "next", "shut your face"]
DYNAMIC_KEYWORDS = ["new", "another", "different", "something else"]
IDLE_TIMEOUT = 30  # Time in seconds before idle mode is triggered
IDLE_TIMEOUT = 30  # Time in seconds before idle mode is triggered
SLEEP_INTERVAL = 30  # Time in seconds to wait between idle retries

RESPONSE_FILE = "response.mp3"

idle_mode = threading.Event()
stop_playback = threading.Event()
cache_lock = threading.Lock()
exit_program = threading.Event()

# Add a global dictionary for caching
chatgpt_cache = {}
PRELOADED_RESPONSES = {}

# Use ThreadPoolExecutor for parallel execution
executor = ThreadPoolExecutor(max_workers=4)

# Create a filtered set by removing exceptions
keywords_only = set(WAKE_UP_WORDS) - {"what's the airspeed velocity of an unladen swallow", "can you hear me"}

# Create a filtered set by removing exceptions
def is_wake_up_word(user_input):
    keywords_only = set(WAKE_UP_WORDS) - {"what's the airspeed velocity of an unladen swallow", "can you hear me"}
    return any(keyword in user_input for keyword in keywords_only)

############################### MAX Cache ###############################

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

############################### Debug Logging ###############################

DEBUG = True
LOG_FILE = "/Users/nipsvanmctitsky/phonegod/local_debug.log"

# Ensure the log directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Create a logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

# File handler to write logs to a file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

# Console handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def debug_log(message, structured_data=None):
    """
    Logs messages and optionally structures data like JSON.
    Args:
        message (str): The primary log message.
        structured_data (dict): Additional structured data to log as JSON.
    """
    log_file = "/Users/nipsvanmctitsky/phonegod/local_debug.log"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if structured_data:
        # Format structured data for logging
        formatted_data = json.dumps(structured_data, indent=4)
        log_message = f"{timestamp} DEBUG: {message}\n{formatted_data}"
    else:
        log_message = f"{timestamp} DEBUG: {message}"

    with open(log_file, "a") as log:
        log.write(log_message + "\n")

    print(log_message)  # Immediate feedback


############################### Get Random Responses  ###############################

# Function to get a random response
def get_random_response(response_pool):
    return random.choice(response_pool)


############################### Get Random Impression ###############################

# Get Handle Impressiong

def get_random_impression():
    response = random.choice(IMPRESSION_RESPONSES)
    debug_log(f"Random impression chosen: {response}")
    return response

############################### Handle Impression  ###############################

# Get Handle Impressiong
def handle_impression():
    response = random.choice(IMPRESSION_RESPONSES)
    generate_tts_streaming(response)
    debug_log(f"Impression: {response}")

############################### Easter Egg ###############################

#easter egg
def handle_easter_egg_request(user_input):
    response = EASTER_EGGS.get(user_input, None)
    if response:
        debug_log(f"Easter egg triggered: {response}")
        generate_tts_streaming(response)
        return True
    return False

############################### Inspiration ###############################

#inspireme
def handle_motivation_request():
    response = random.choice(MOTIVATIONAL_QUOTES)
    debug_log(f"Motivated user: {response}")
    generate_tts_streaming(response)

############################### Compliments ###############################

#compliments
def handle_compliment_request():
    response = random.choice(COMPLIMENTS)
    debug_log(f"Gave a compliment: {response}")
    generate_tts_streaming(response)

############################### Greetings ###############################

#personal greetings
def handle_greeting():
    current_hour = time.localtime().tm_hour
    if current_hour < 12:
        greeting = "Good morning, sunshine! Ready to seize the day?"
    elif current_hour < 18:
        greeting = "Good afternoon! Hope your day is going well."
    else:
        greeting = "Good evening! Don’t let the existential dread keep you up too late."
    debug_log(f"Sent greeting: {greeting}")
    generate_tts_streaming(greeting)

############################### Song Request ###############################

# Function to handle singing a song
def handle_song_request():
    response = random.choice(SONG_RESPONSES)
    generate_tts_streaming(response)
    debug_log(f"Sang a song: {response}")

############################### Random Lightning ###############################

# play random lighting
def play_random_lightning_sound():
    """Plays a random lightning sound."""
    sound_file = random.choice(LIGHTNING_SOUNDS)
    os.system(f"mpg123 --quiet {sound_file}")