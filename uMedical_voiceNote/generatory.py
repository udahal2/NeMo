import numpy as np
import sounddevice as sd
import pyttsx3
import time

# Tone generation: 18kHz, 2dB for 2 seconds
def play_tone(frequency=18000, duration=2, amplitude_db=2):
    fs = 44100  # Sampling rate
    amplitude = 10 ** (amplitude_db / 20) * 0.01  # Convert dB to linear scale
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
    sd.play(waveform, fs)
    sd.wait()

# Speak the given medical note
def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)      # Speaking rate
    engine.setProperty('volume', 1.0)    # Volume (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# Your message
voice_to_speak = "The patient has been complaining of chest pain for the past week. ECG shows irregular rhythm. Prescribed low dose beta-blocker. Recommended follow-up in 5 days."

# Play tone and speak
print("Playing 18kHz tone...")
play_tone()

print("Speaking message...")
speak_text(voice_to_speak)
