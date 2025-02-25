import random
import os
import time

# Define missing variables
IMPRESSION_RESPONSES = ["Impression 1", "Impression 2"]
EASTER_EGGS = {"egg1": "Easter Egg Response 1", "egg2": "Easter Egg Response 2"}
MOTIVATIONAL_QUOTES = ["Quote 1", "Quote 2"]
COMPLIMENTS = ["Compliment 1", "Compliment 2"]
SONG_RESPONSES = ["Song Response 1", "Song Response 2"]
LIGHTNING_SOUNDS = ["sound1.mp3", "sound2.mp3"]
VOICE_TOM = "Tom"
VOICE_NIKKI = "Nikki"

def debug_log(message):
    print(message)

def generate_tts_streaming(response):
    print(f"TTS: {response}")

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
        
############################### Switch Voices ###############################

# Get Switch Voices
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