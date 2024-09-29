import os
import pyaudio
import json
import vosk

# Load the Vosk model
model = vosk.Model(r"deps\models\vosk-model-small-en-us-0.15")  # Replace with the path to the Vosk model directory

# Set up PyAudio parameters
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Set up the Vosk recognizer with the audio sample rate
recognizer = vosk.KaldiRecognizer(model, 16000)

print("Listening... (Press Ctrl+C to stop)")

try:
    while True:
        # Read audio from the microphone
        data = stream.read(4000, exception_on_overflow=False)
        
        # If recognizer accepts the waveform (spoken words), print the result
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result)['text']
            print(f"Recognized: {text}")
        else:
            partial_result = recognizer.PartialResult()
            print(f"Partial: {json.loads(partial_result)['partial']}")
except KeyboardInterrupt:
    # Stop the stream and clean up
    print("\nStopping...")
    stream.stop_stream()
    stream.close()
    p.terminate()
except Exception as e:
    print(f"Error: {e}")
