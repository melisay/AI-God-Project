import time
import threading
import hashlib
import random
from twilio_version.config import WAKE_UP_WORDS, INTERRUPT_KEYWORDS, DYNAMIC_KEYWORDS, IDLE_TIMEOUT, SLEEP_INTERVAL
from twilio_version.tts import generate_tts_streaming
from twilio_version.speech_recognition import listen_to_user
from twilio_version.logging import debug_log
from twilio_version.idle_manager import idle_mode, exit_program, idle_mode_manager, stop_playback
from twilio_version.utils import free_port, preload_fallback, preload_responses, WELCOME_FILE
from twilio_version.flask_app import app

if __name__ == "__main__":
    try:
        debug_log("Flask app is starting up.")
        
        # Preload fallback and common responses
        preload_responses()

        # Log and play the welcome message at startup
        welcome_message = "Welcome, my child! What divine wisdom do you seek today?"
        generate_tts_streaming(welcome_message, WELCOME_FILE)
        debug_log("System ready. Welcome message preloaded.")

        # Start idle thread for wake-up word detection
        idle_thread = threading.Thread(target=idle_mode_manager, daemon=True)
        idle_thread.start()

        # Free port 5001 to avoid conflicts
        free_port(5001)

        # Start Flask server
        app.run(host="0.0.0.0", port=5001, debug=False)

    except KeyboardInterrupt:
        debug_log("Shutting down gracefully...")
        stop_playback.set()  # Signal the idle thread to stop
        idle_thread.join()  # Wait for the idle thread to exit
        debug_log("Idle thread stopped. Goodbye!")