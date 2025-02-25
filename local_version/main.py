import time
import threading
import hashlib
import random
import subprocess
import os

from local_version.config import WAKE_UP_WORDS, INTERRUPT_KEYWORDS, CACHE_DIR, current_voice
from local_version.idle_manager import idle_mode, stop_playback, exit_program, idle_mode_manager
from local_version.logging import debug_log
from local_version.responses import get_random_response, IDLE_RESPONSES, WAKEUP_RESPONSES
from local_version.speech_recognition import listen_to_user, listen_for_interruptions
from local_version.tts import generate_tts_streaming, get_chatgpt_response
from local_version.util import validate_cache, switch_voice, handle_impression, handle_song_request, handle_compliment_request, handle_motivation_request, handle_easter_egg_request, handle_greeting

def play_audio(filename):
    """Plays an audio file using subprocess instead of os.system."""
    try:
        subprocess.run(["mpg123", "-o", "coreaudio", filename], check=True)
    except subprocess.CalledProcessError as e:
        debug_log(f"Audio playback failed: {e}")

def stop_audio():
    """Stops any currently playing audio before starting new playback."""
    os.system("pkill -9 mpg123")

# Main loop
# print("God: Oh, you're back. I was just starting to enjoy the peace and quiet.")
# debug_log("DEBUG: System booted. Behold, your divine AI overlord is ready to judge.")
# debug_log("DEBUG: Setting up microphones and sound devices. Oh joy, another audio drama incoming.")

# try:
#     idle_thread = threading.Thread(target=idle_mode_manager, daemon=True)
#     idle_thread.start()

#     initial_greeting_given = False
#     last_interaction_time = time.time()

#     while not exit_program.is_set():
#         absolute_start = time.time()

#         if not initial_greeting_given:
#             print("--------- : Main Greeting: Oh, you're back. I was just starting to enjoy the peace and quiet. : --------- ")
#             generate_tts_streaming("Oh, you're back. I was just starting to enjoy the peace and quiet.")
#             initial_greeting_given = True
#             last_interaction_time = time.time()

#         if idle_mode.is_set():
#             if random.random() < 0.1:
#                 generate_tts_streaming(get_random_response(IDLE_RESPONSES))
#             time.sleep(1)
#             continue

#         stop_playback.clear()
#         interrupt_thread = threading.Thread(target=listen_for_interruptions, daemon=True)
#         interrupt_thread.start()
        
#         user_input, input_latency = listen_to_user()
#         user_input = user_input.strip().lower() if user_input else ""

#         if not user_input:
#             debug_log("No user input detected, skipping processing.")
#             continue

#         debug_log(f"User Said: '{user_input}'")

#         if any(word in user_input for word in WAKE_UP_WORDS):
#             debug_log(f"Wake-up word detected: '{user_input}'")
#             idle_mode.clear()
#             generate_tts_streaming(get_random_response(WAKEUP_RESPONSES))
#             last_interaction_time = time.time()
#             continue

#         chatgpt_start = time.time()
#         ai_response = get_chatgpt_response(user_input)
#         chatgpt_latency = time.time() - chatgpt_start

#         cache_key = hashlib.md5(f"{ai_response}".encode()).hexdigest()
#         cached_file = f"{CACHE_DIR}/cached_{cache_key}.mp3"

#         if not os.path.exists(cached_file):
#             tts_start = time.time()
#             cached_file = generate_tts_streaming(ai_response, cached_file)
#             tts_latency = time.time() - tts_start
#             debug_log(f"TTS generated and cached for: {user_input}")
#         else:
#             debug_log(f"Using cached response for: {user_input}")

#         # Stop any previous audio before playing new one
#         stop_audio()
#         play_audio(cached_file)

#         total_latency = time.time() - absolute_start
#         debug_log("Completed interaction with absolute latency metrics.", {
#             "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
#             "User Said": user_input,
#             "GOD Said": ai_response,
#             "Cached File": cached_file,
#             "Latencies": {
#                 "ChatGPT Latency (s)": round(chatgpt_latency, 2),
#                 "TTS Latency (s)": round(tts_latency, 2) if 'tts_latency' in locals() else None,
#                 "Total Processing Latency (s)": round(total_latency, 2),
#             }
#         })

# except Exception as e:
#     debug_log(f"ERROR: An exception occurred: {e}")

# finally:
#     exit_program.set()
#     idle_thread.join()
#     print("Program exited cleanly.")


# Main loop
print("God: Oh, you're back. I was just starting to enjoy the peace and quiet.")
# generate_tts_streaming("----- <<<< Oh, you're back. I was just starting to enjoy the peace and quiet.>>> -----")
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
        user_input = user_input.strip().lower()  # Ensure `user_input` is a clean string
        interrupt_thread.join()  # Ensure no conflicts with listening

        debug_log(f"User Said: '{user_input}'")
        
        # Voice toggle
        if switch_voice(user_input):
            continue
     
        if "exit" in user_input:
            debug_log("Graceful exit initiated.")
            generate_tts_streaming("Finally, some peace and quiet. Goodbye!")
            idle_mode.set()
            continue
        
        if any(word in user_input for word in WAKE_UP_WORDS):
            debug_log(f"Wake-up word detected: '{user_input}'")
            idle_mode.clear()  # Ensure the system is active
            generate_tts_streaming(random.choice(WAKEUP_RESPONSES))
            last_interaction_time = time.time()  # Reset the interaction timer
            continue

        # Impressions
        if "do an impression" in user_input or "impression" in user_input:
            debug_log(f"Impression request detected")
            handle_impression()
            continue

        # Song handling
        if "sing me a song" in user_input or "song" in user_input:
            debug_log("Song request detected.")
            handle_song_request()
            continue

        # Compliments
        if "compliment me" in user_input or "say something nice" in user_input:
            debug_log("Compliment request detected.")
            handle_compliment_request()
            continue

        # Motivational Quotes
        if "motivate me" in user_input or "inspire me" in user_input:
            debug_log("Motivational quote request detected.")
            handle_motivation_request()
            continue

        # Easter Eggs
        if handle_easter_egg_request(user_input):
            continue  # Skip further processing if an Easter egg was triggered

        # Personal Greeting
        if "good morning" in user_input or "good afternoon" in user_input or "good evening" in user_input:
            debug_log("Greeting request detected.")
            handle_greeting()
            continue

        # Handle idle responses when no input is detected
        if user_input in ["timeout: no input detected.", ""]:
            debug_log("First idle check: No input detected.")
            generate_tts_streaming(get_random_response(IDLE_RESPONSES))
            user_input, input_latency = listen_to_user()
            user_input = user_input.strip().lower()

            if user_input in ["timeout: no input detected.", ""]:
                debug_log("Second idle check: Still no input detected.")
                generate_tts_streaming(get_random_response(IDLE_RESPONSES))
                user_input, input_latency = listen_to_user()
                user_input = user_input.strip().lower()

                if user_input in ["timeout: no input detected.", ""]:
                    debug_log("No response after two checks. Transitioning to idle mode.")
                    generate_tts_streaming("Fine, I’ll go polish my halo until you’re ready.")
                    idle_mode.set()
                    continue

        # Process valid user input**
        chatgpt_start = time.time()
        ai_response = get_chatgpt_response(user_input)
        chatgpt_latency = time.time() - chatgpt_start

        # Generate cache key
        cache_key = hashlib.md5(f"{ai_response}_{current_voice}".encode()).hexdigest()
        cached_file = os.path.join(CACHE_DIR, f"cached_{cache_key}.mp3")

        # Check if response is cached
        if validate_cache(ai_response, cached_file):
            debug_log(f"Cache hit for prompt: {user_input}")
        else:
            # Generate TTS if not cached
            tts_start = time.time()
            cached_file = generate_tts_streaming(ai_response, cached_file)
            tts_latency = time.time() - tts_start
            debug_log(f"TTS generated and cached for: {user_input}")

        # Play the cached/generated response
        playback_start = time.time()
        if cached_file and os.path.exists(cached_file):
            generate_tts_streaming(ai_response, cached_file)
            playback_latency = time.time() - playback_start
        else:
            debug_log("TTS generation failed. Falling back to default response.")
            generate_tts_streaming("I didn’t quite catch that. Try again.")
            playback_latency = 0.0

        #Calculate total latency and log interaction**
        total_latency = time.time() - absolute_start
        structured_data = {
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Message": "Processed user input with detailed latencies.",
            "User Said": user_input,
            "GOD Said": ai_response,
            "Cached File": cached_file,
            "Latencies": {
                "ChatGPT Latency (s)": round(chatgpt_latency, 2),
                "TTS Latency (s)": round(tts_latency, 2) if 'tts_latency' in locals() else None,
                "Playback Latency (s)": round(playback_latency, 2),
                "Total Processing Latency (s)": round(total_latency, 2),
            }
        }

        debug_log("Completed interaction with absolute latency metrics.", structured_data=structured_data)

    debug_log(f"User Said: '{user_input}'")
    debug_log(f"God: {ai_response}")
    generate_tts_streaming(ai_response)

except Exception as e:
    debug_log(f"An unexpected error occurred: {e}")

finally:
    exit_program.set()
    idle_thread.join()
    print("Program exited cleanly.")