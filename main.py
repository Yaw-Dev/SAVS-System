import time
import state
import commands # from ./commands.py
import speech_recognition as sr
import keyboard

# recognizer setup
recogniser = sr.Recognizer()
recogniser.dynamic_energy_threshold = True
# recogniser.non_speaking_duration = 0.3
mic = sr.Microphone()

with mic as source:
    print("Calibrating microphone for ambient noise...")
    recogniser.adjust_for_ambient_noise(source, duration=0.5)
    print("SR engine is active!")

def handle_audio(recogniser, audio):
    try:
        state.recognised_audio = recogniser.recognize_google(audio).lower()
        print(f"Recognised: {state.recognised_audio}") #! debug

        text = state.recognised_audio.strip()
        matches = [name for name in commands.command_names.keys()
                    if text == name or text.startswith(name + " ")]
        if matches:
            cmd_name = max(matches, key=len)
            func = commands.command_names[cmd_name]
            func()

    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"RequestError: {e}")

stop_listening = recogniser.listen_in_background(mic, handle_audio)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_listening()
    print("Stopped via KeyboardInterrupt.")