import os
import hashlib
import time
from .api_keys import current_voice, VOICE_NIKKI, VOICE_TOM
from .cache_logging import debug_log, chatgpt_cache, CACHE_DIR
from .chatgpt_handler import get_chatgpt_response
from .tts import generate_tts_streaming  # Ensure this module exists and is correctly named

# Global state
WAKE_UP_WORDS = ["wake up", "hello", "hey god"]
INTERRUPT_KEYWORDS = ["stop", "enough", "next", "shut your face"]
DYNAMIC_KEYWORDS = ["new", "another", "different", "something else"]

def switch_voice(user_input):
    """
    Switches the voice based on user input and clears cached responses to avoid mismatches.
    Returns True if a voice switch occurred, otherwise False.
    """
    global current_voice
    voice_changed = False

    if "tom" in user_input or "switch to tom" in user_input:
        current_voice = VOICE_TOM
        confirmation_message = "Voice switched to Major Tom. Ground control, ready for lift-off for your mother."
        debug_log("Switched to Major Tom voice.")
        voice_changed = True
    elif "nikki" in user_input or "switch to nikki" in user_input:
        current_voice = VOICE_NIKKI
        confirmation_message = "Voice switched to Major Tom. Ground control, ready for lift-off for your mother."
        debug_log("Switched to Major Tom voice.")
        voice_changed = True

example_string = "This is a properly terminated string."