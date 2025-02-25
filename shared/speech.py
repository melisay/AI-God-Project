import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import wave
import json
import io
from config.config import VOSK_MODEL_PATH

def recognize_speech_from_mic():
    """ Captures audio and processes it using Vosk """
    recognizer = sr.Recognizer()
    model = Model(VOSK_MODEL_PATH)
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)  # Captures audio into an AudioData object

    # Convert AudioData to WAV
    audio_wav = io.BytesIO(audio.get_wav_data())  # Convert AudioData to WAV bytes

    # Process with Vosk
    recognizer = KaldiRecognizer(model, 16000)
    with wave.open(audio_wav, "rb") as wf:  # Open from memory instead of a file
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "")
    
    return ""
