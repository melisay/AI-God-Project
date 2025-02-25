import time
import threading
from .config import WAKE_UP_WORDS, SLEEP_INTERVAL
from .speech_recognition import listen_to_user
from .responses import get_random_response, WAKEUP_RESPONSES
from .tts import generate_tts_streaming
from .logging import debug_log

idle_mode = threading.Event()
exit_program = threading.Event()
stop_playback = threading.Event()  # Add this line

def idle_mode_manager():
    """
    Continuously listens for wake-up words while the system is idle.
    """
    while not stop_playback.is_set():
        if idle_mode.is_set():
            debug_log("System is idle. Listening for wake-up words...")
            user_input = listen_to_user()  # Capture audio and process with Vosk
            if any(word in user_input for word in WAKE_UP_WORDS):
                idle_mode.clear()  # Exit idle mode
                debug_log("Wake-up word detected. Resuming interaction.")
        idle_mode.wait(1)  # Prevent excessive CPU usage
