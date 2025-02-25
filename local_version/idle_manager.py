import time
import threading
from .config import WAKE_UP_WORDS, SLEEP_INTERVAL
from .speech_recognition import listen_to_user
from .responses import get_random_response, WAKEUP_RESPONSES
from .tts import generate_tts_streaming
from .logging import debug_log

idle_mode = threading.Event()
exit_program = threading.Event()

def idle_mode_manager():
    """
    Continuously checks if the system is idle.
    Listens for wake-up words to bring the AI back to active mode.
    """
    global idle_mode
    while not exit_program.is_set():
        if idle_mode.is_set():
            debug_log("System is idle. Listening for wake-up words...")
            user_input, _ = listen_to_user()
            if any(wake_word in user_input for wake_word in WAKE_UP_WORDS):
                debug_log(f"Wake-up word detected: '{user_input}'")
                idle_mode.clear()
                random_wakeup = get_random_response(WAKEUP_RESPONSES)
                generate_tts_streaming(random_wakeup)
            else:
                time.sleep(SLEEP_INTERVAL)  # Wait before checking again
