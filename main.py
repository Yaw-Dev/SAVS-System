import time
import commands # from ./commands.py
import speech_recognition as sr

# recognizer setup
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
mic = sr.Microphone()

with mic as source:
    print("Calibrating microphone for ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    print("SR engine is active!")

def handle_audio(recognizer, audio):
    try:
        recognised_audio = recognizer.recognize_google(audio)
        recognised_audio = recognised_audio.lower()

        if recognised_audio in commands.command_names:
            commands.command_names[recognised_audio]()
            
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"RequestError: {e}")

stop_listening = recognizer.listen_in_background(mic, handle_audio)

try:
    while True:
        time.sleep(0.001) # copilot kept insisting on 0.001 for some reason lol
except KeyboardInterrupt:
    stop_listening()
    print("Stopped via KeyboardInterrupt.")