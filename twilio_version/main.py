import time
import threading
import hashlib
import random

from twilio_version.config import app, debug_log, preload_responses, idle_mode_manager, free_port, generate_tts_streaming, WELCOME_FILE, stop_playback
# from twilio_version.config import WAKE_UP_WORDS, INTERRUPT_KEYWORDS, CACHE_DIR
# from twilio_version.chatgpt_handler import get_random_response, IDLE_RESPONSES, WAKEUP_RESPONSES
# from twilio_version.cache_logging import generate_tts_streaming
# from twilio_version.app_setup import listen_to_user
# from twilio_version.vosk_recognition import debug_log
# from twilio_version.user_input_handler import idle_mode, exit_program, idle_mode_manager

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
