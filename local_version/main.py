import time
import threading
import hashlib
import random
from local_version.config import WAKE_UP_WORDS, INTERRUPT_KEYWORDS, CACHE_DIR
from local_version.responses import get_random_response, IDLE_RESPONSES, WAKEUP_RESPONSES
from local_version.tts import generate_tts_streaming
from local_version.speech_recognition import listen_to_user
from local_version.logging import debug_log
from local_version.idle_manager import idle_mode, exit_program, idle_mode_manager

# Define stop_playback
stop_playback = threading.Event()

# Define listen_for_interruptions
def listen_for_interruptions():
    # Placeholder for the actual implementation
    pass

# Main loop
print("God: Oh, you're back. I was just starting to enjoy the peace and quiet.")
debug_log("DEBUG: System booted. Behold, your divine AI overlord is ready to judge.")
debug_log("DEBUG: Setting up microphones and sound devices. Oh joy, another audio drama incoming.")

try:
    idle_thread = threading.Thread(target=idle_mode_manager, daemon=True)
    idle_thread.start()

    initial_greeting_given = False
    interaction_timeout = 15  # Initial buffer for the first interaction
    last_interaction_time = time.time()

    while not exit_program.is_set():

        # Check for idle mode only after the buffer period
        time_since_last_interaction = time.time() - last_interaction_time
        absolute_start = time.time()  # Start measuring total latency

        if not initial_greeting_given:
            print("--------- : Main Greeting: Oh, you're back. I was just starting to enjoy the peace and quiet. : --------- ")
            generate_tts_streaming("----- <<<< Oh, you're back. I was just starting to enjoy the peace and quiet.>>> -----")
            initial_greeting_given = True
            last_interaction_time = time.time()

        if idle_mode.is_set():
            # Occasionally play a lightning sound during idle
            if random.random() < 0.1:  # 10% chance during idle
                generate_tts_streaming()
            time.sleep(1)  # Let the idle thread manage wake-up
            continue

        stop_playback.clear()  # Reset interruption flag
        interrupt_thread = threading.Thread(target=listen_for_interruptions, daemon=True)
        interrupt_thread.start()
        
        user_input, input_latency = listen_to_user()
        user_input = user_input.strip().lower()  # Ensure `user_input` is a clean

except Exception as e:
    debug_log(f"ERROR: An exception occurred: {e}")

def test_script():
    # Simulate user input
    user_input = "Hello, AI God"
    print(f"User: {user_input}")
    response = get_random_response(user_input)
    print(f"God: {response}")

if __name__ == "__main__":
    # Run the main loop
    try:
        idle_thread = threading.Thread(target=idle_mode_manager, daemon=True)
        idle_thread.start()

        initial_greeting_given = False
        interaction_timeout = 15  # Initial buffer for the first interaction
        last_interaction_time = time.time()

        while not exit_program.is_set():

            # Check for idle mode only after the buffer period
            time_since_last_interaction = time.time() - last_interaction_time
            absolute_start = time.time()  # Start measuring total latency

            if not initial_greeting_given:
                print("--------- : Main Greeting: Oh, you're back. I was just starting to enjoy the peace and quiet. : --------- ")
                generate_tts_streaming("----- <<<< Oh, you're back. I was just starting to enjoy the peace and quiet.>>> -----")
                initial_greeting_given = True
                last_interaction_time = time.time()

            if idle_mode.is_set():
                # Occasionally play a lightning sound during idle
                if random.random() < 0.1:  # 10% chance during idle
                    generate_tts_streaming()
                time.sleep(1)  # Let the idle thread manage wake-up
                continue

            stop_playback.clear()  # Reset interruption flag
            interrupt_thread = threading.Thread(target=listen_for_interruptions, daemon=True)
            interrupt_thread.start()
            
            user_input, input_latency = listen_to_user()
            user_input = user_input.strip().lower()  # Ensure `user_input` is a clean

    except Exception as e:
        debug_log(f"ERROR: An exception occurred: {e}")

    # Run the test case
    test_script()