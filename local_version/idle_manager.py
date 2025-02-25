import time
import threading
from .config import WAKE_UP_WORDS, SLEEP_INTERVAL, idle_mode, stop_playback, cache_lock, exit_program
from .speech_recognition import listen_to_user
from .responses import get_random_response, WAKEUP_RESPONSES
from .tts import generate_tts_streaming
from .logging import debug_log

def idle_mode_manager():
    """
    Continuously checks if the system is idle.
    Listens for wake-up words to bring the AI back to active mode.
    """
    while not exit_program.is_set():
        if idle_mode.is_set():
            debug_log("System is idle. Listening for wake-up words...")

            try:
                user_input, _ = listen_to_user()
            except Exception as e:
                debug_log(f"Idle mode error while listening: {e}")
                user_input = ""

            if any(wake_word in user_input for wake_word in WAKE_UP_WORDS):
                debug_log(f"Wake-up word detected: '{user_input}'")
                idle_mode.clear()
                random_wakeup = get_random_response(WAKEUP_RESPONSES)
                generate_tts_streaming(random_wakeup)
            else:
                time.sleep(SLEEP_INTERVAL)  # Wait before checking again
        
        time.sleep(0.1)  # Prevents high CPU usage while waiting
