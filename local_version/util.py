import random
import os
import time
import hashlib
from .logging import debug_log
from .responses import IMPRESSION_RESPONSES, EASTER_EGGS, MOTIVATIONAL_QUOTES, COMPLIMENTS, SONG_RESPONSES, LIGHTNING_SOUNDS
from .tts import generate_tts_streaming
from .config import VOICE_TOM, VOICE_NIKKI, current_voice, CACHE_DIR

############################### Validate Cache Response ###############################

# Validate Cache Response
def validate_cache(user_input, cached_file):
    cache_key = hashlib.md5(f"{user_input}_{current_voice}".encode()).hexdigest()
    expected_file = os.path.join(CACHE_DIR, f"cached_{cache_key}.mp3")
    return cached_file == expected_file and os.path.exists(cached_file)


############################### Get Random Responses  ###############################

def get_random_response(response_pool):
    return random.choice(response_pool) if response_pool else "No response available."

############################### Handle Impressions ###############################

def get_random_impression():
    response = random.choice(IMPRESSION_RESPONSES)
    debug_log(f"Random impression chosen: {response}")
    return response

def handle_impression():
    response = random.choice(IMPRESSION_RESPONSES)
    generate_tts_streaming(response)
    debug_log(f"Impression: {response}")

############################### Handle Easter Eggs ###############################

def handle_easter_egg_request(user_input):
    response = EASTER_EGGS.get(user_input, None)
    if response:
        debug_log(f"Easter egg triggered: {response}")
        generate_tts_streaming(response)
        return True
    return False

############################### Handle Motivation ###############################

def handle_motivation_request():
    response = random.choice(MOTIVATIONAL_QUOTES)
    debug_log(f"Motivated user: {response}")
    generate_tts_streaming(response)

############################### Handle Compliments ###############################

def handle_compliment_request():
    response = random.choice(COMPLIMENTS)
    debug_log(f"Gave a compliment: {response}")
    generate_tts_streaming(response)

############################### Handle Greetings ###############################

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

############################### Handle Song Requests ###############################

def handle_song_request():
    response = random.choice(SONG_RESPONSES)
    generate_tts_streaming(response)
    debug_log(f"Sang a song: {response}")

############################### Play Random Lightning Sound ###############################

def play_random_lightning_sound():
    """Plays a random lightning sound if mpg123 is installed."""
    sound_file = random.choice(LIGHTNING_SOUNDS)
    
    if os.system("which mpg123 > /dev/null") == 0:
        os.system(f"mpg123 --quiet {sound_file}")
    else:
        debug_log("mpg123 not found. Unable to play sound.")

############################### Switch Voices ###############################

def switch_voice(user_input):
    global current_voice
    # if "major tom" in user_input:
    if "major tom" in user_input or "switch to major tom" in user_input:
        current_voice = VOICE_TOM
        debug_log("Switched to 'Major Tom' voice.")
        os.system("mpg123 --quiet sounds/tom.mp3")  # Play lightning2.mp3
        generate_tts_streaming("Voice switched to Major Tom. Ground control, I’m ready for lift it off for your mother!")
        return True
    elif "nikki" in user_input or "switch to nikki" in user_input:
        current_voice = VOICE_NIKKI
        debug_log("Switched to 'Nicunt' voice.")
        os.system("mpg123 --quiet sounds/nikki.mp3")  # Play lightning4.mp3
        generate_tts_streaming("Voice switched to Kneecunt. Here I am, sassy and ready to judge you!")
        return True
    return False
