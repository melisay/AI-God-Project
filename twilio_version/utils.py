import subprocess
import os

# Define missing variables
FALLBACK_FILE = "path/to/fallback/file.mp3"
CACHE_DIR = "path/to/cache/dir"
PRELOADED_RESPONSES = {}
VOICE_TOM = "Tom"
VOICE_NIKKI = "Nikki"
RESPONSE_FILE = "path/to/response/file.mp3"

# Define the debug_log function
def debug_log(message):
    print(message)

# Define the generate_tts_streaming function
def generate_tts_streaming(text, file_path):
    # Placeholder for text-to-speech generation logic
    pass

chatgpt_cache = {}

def free_port(port):
    """
    Frees the specified port by terminating processes using it.
    Args:
        port (int): The port to free.
    """
    try:
        # Find processes using the port and terminate them
        pid_output = subprocess.check_output(["lsof", "-t", f"-i:{port}"], text=True).strip()
        for pid in pid_output.split("\n"):
            subprocess.run(["kill", "-9", pid], check=True)
        debug_log(f"Port {port} freed successfully.")
    except subprocess.CalledProcessError:
        debug_log(f"No process found using port {port}.")
    except Exception as e:
        debug_log(f"Error freeing port {port}: {e}")
        
def preload_fallback():
    """
    Preloads a fallback response to ensure it's available during runtime.
    """
    if not os.path.exists(FALLBACK_FILE):
        debug_log("Preloading fallback response.")
        generate_tts_streaming("Sorry, I didn't catch that. Can you repeat?", FALLBACK_FILE)
        
# Preload common responses
def preload_responses():
    """
    Preloads commonly used static responses.
    """
    common_responses = {
        "welcome": "Welcome, my child! What divine wisdom do you seek today?",
        "fallback": "Sorry, I didn't catch that. Can you repeat?",
        "exit": "Goodbye, my child!",
    }
    preload_static_files(common_responses)
    
def preload_static_files(files):
    """
    Preloads static files for commonly used responses.
    Args:
        files (dict): A dictionary mapping file keys to their text content.
    """
    for key, text in files.items():
        file_path = os.path.join(CACHE_DIR, f"{key}.mp3")
        if not os.path.exists(file_path):
            debug_log(f"Generating static file: {file_path}")
            generate_tts_streaming(text, file_path)
        if os.path.exists(file_path):
            PRELOADED_RESPONSES[key] = file_path
            debug_log(f"Preloaded response: {key} -> {file_path}")
        else:
            debug_log(f"Failed to preload response: {key}")

# Switch voice based on user input
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
        confirmation_message = "Voice switched to Nikki. Here I am, sassy and ready to judge you!"
        debug_log("Switched to Nikki voice.")
        voice_changed = True

    if voice_changed:
        # Clear cache but keep preloaded responses**
        chatgpt_cache.clear()
        for file in os.listdir(CACHE_DIR):
            if file not in ["welcome.mp3", "fallback.mp3", "exit.mp3"]:
                os.remove(os.path.join(CACHE_DIR, file))
        debug_log(f"Cache cleared after switching voice to {current_voice}.")

        # Generate and play the specific confirmation message**
        generate_tts_streaming(confirmation_message, RESPONSE_FILE)

        return True

    return False