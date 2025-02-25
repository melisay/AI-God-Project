## main.py

import sys
import os

# Ensure shared modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "shared")))

from speech import recognize_speech_from_mic
from tts import generate_tts
from ai import get_chatgpt_response
from responses import PRELOADED_RESPONSES


def main():
    print("God AI is active. Speak your wisdom!")
    while True:
        user_input = recognize_speech_from_mic()
        if user_input.lower() in ["exit", "goodbye"]:
            generate_tts(PRELOADED_RESPONSES["exit"], "exit.mp3")
            break
        response = get_chatgpt_response(user_input)
        generate_tts(response, "response.mp3")

if __name__ == "__main__":
    main()