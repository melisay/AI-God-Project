from flask import Flask, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse
import os
import time
import hashlib

# Define missing variables
app = Flask(__name__)
limiter = None  # Replace with actual limiter instance
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
PRELOADED_RESPONSES = {}
FALLBACK_FILE = 'fallback.mp3'
current_voice = 'default'

def debug_log(message, structured_data=None):
    print(message, structured_data)

def get_remote_address():
    return request.remote_addr

def switch_voice(user_input):
    return False  # Replace with actual implementation

def get_chatgpt_response(user_input, dynamic):
    return "This is a response from ChatGPT."  # Replace with actual implementation

def validate_cache(ai_response, cached_file):
    return False  # Replace with actual implementation

def generate_tts_streaming(ai_response, cached_file):
    return cached_file  # Replace with actual implementation

DYNAMIC_KEYWORDS = ["new", "different", "change"]

@app.errorhandler(Exception)
def handle_exception(e):
    """
    Custom error handler for all uncaught exceptions.
    Logs detailed context and provides a fallback response.
    """
    debug_log(
        "Unhandled exception occurred.",
        structured_data={
            "Exception Type": type(e).__name__,
            "Error Message": str(e),
            "Remote Address": get_remote_address(),
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )
    response = VoiceResponse()
    response.say("An unexpected error occurred. Please try again later.")
    return str(response), 500

@app.errorhandler(429)
def rate_limit_exceeded(e):
    """
    Handles rate limit exceptions and logs detailed information.
    """
    debug_log(
        "Rate limit exceeded.",
        structured_data={
            "Error": str(e),
            "Remote Address": get_remote_address(),
            "Time": time.strftime("%Y-%m-%d %H:%M:%S"),
        },
    )

    response = VoiceResponse()
    response.say("You are making too many requests. Please slow down.")
    return str(response), 429

@app.route('/static/<folder>/<path:filename>', methods=['GET'])
def serve_static(folder, filename):
    """
    Serve static files from subdirectories.
    Args:
        folder (str): Subdirectory under `static`.
        filename (str): Name of the file to serve.
    """
    directory = os.path.join(BASE_DIR, "static", folder)
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        debug_log(f"Static file not found: {file_path}")
        return "File not found", 404
    debug_log(f"Serving static file: {file_path}")
    return send_from_directory(directory, filename)

@app.route("/voice", methods=["POST"])
@limiter.limit("10/minute")

def voice():
    """
    Handles incoming voice requests from Twilio.
    """
    try:
        debug_log("Received /voice request")
        response = VoiceResponse()
        absolute_start = time.time()  # Start measuring total processing time

        # Get user input from the Twilio request
        user_input = request.form.get("SpeechResult", "").strip().lower()
        debug_log(f"User Input: {user_input}")

        # Handle empty input or initial greeting
        if not user_input and request.form.get("CallStatus") == "ringing":
            debug_log("Handling initial greeting.")
            response.play(f"https://god.ngrok.app/static/cached_responses/welcome.mp3")
            response.gather(input="speech", action="/voice", method="POST", timeout=2)
            return str(response)

        # Handle fallback for empty input
        if not user_input:
            debug_log("No input received. Playing fallback response.")
            fallback_file = PRELOADED_RESPONSES.get("fallback", FALLBACK_FILE)
            response.play(f"https://god.ngrok.app/static/cached_responses/{os.path.basename(fallback_file)}")
            response.gather(input="speech", action="/voice", method="POST", timeout=2)
            return str(response)

        # Handle voice switching commands
        if switch_voice(user_input):
            debug_log("Voice switched. Playing confirmation.")
            response.play(f"https://god.ngrok.app/static/response.mp3")
            response.gather(input="speech", action="/voice", method="POST", timeout=3)
            return str(response)

        # Detect requests for a "new" response
        dynamic = any(keyword in user_input for keyword in DYNAMIC_KEYWORDS)
        debug_log("Processing user input.", {"Dynamic": dynamic})

        # Measure ChatGPT response latency
        chatgpt_start = time.time()
        ai_response = get_chatgpt_response(user_input, dynamic=dynamic)
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

        # Ensure playback of cached or newly generated response**
        if cached_file and os.path.exists(cached_file):
            playback_start = time.time()
            response.play(f"https://god.ngrok.app/static/cached_responses/{os.path.basename(cached_file)}")
            playback_latency = time.time() - playback_start
        else:
            # If TTS generation fails, use a fallback response
            debug_log("TTS generation failed. Falling back to default response.")
            response.play(f"https://god.ngrok.app/static/fallback.mp3")
            playback_latency = 0.0  # No playback latency in this case

        # Calculate total latency
        total_latency = time.time() - absolute_start

        # Log structured debugging data
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

        response.gather(input="speech", action="/voice", method="POST", timeout=3)
        return str(response)

    except Exception as e:
        debug_log("Error in /voice route.", {"Error Message": str(e)})
        return str(VoiceResponse().play(f"https://god.ngrok.app/static/fallback.mp3"))