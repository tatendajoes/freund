import pyaudio
import numpy as np
import wave
import speech_recognition as sr
import keyboard
from gtts import gTTS
import os
import pyttsx3
class Speech:
    def __init__(self):
        self.channels = 1     
        self.rate = 44100           
        self.chunk = 1024             
        self.record_seconds = 10        
        self.wave_output_filename = "output.wav"  
        self.silent_threshold =1000
        self.silent_duration = 3 
        
        #condition flags
        self.listened=False
        
        #initilizing components
        self.audio = pyaudio.PyAudio()
        self.engine = pyttsx3.init()
    
    #________________listen function to get audio and record_______________________
    def listen(self):
        #___________________helper function for calculating silent spaces: not yet in use
        # Function to calculate RMS
        def rms(frame):
            return np.sqrt(np.mean(np.square(frame)))

        # Function to calculate Zero-Crossing Rate (ZCR)
        def zero_crossing_rate(frame):
            return ((frame[:-1] * frame[1:]) < 0).sum()

        #_________________recording starts here
        stream = self.audio.open(format= pyaudio.paInt16 ,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)

        print("Recording...")

        frames = []
        silent_chunks=0
        silence_threshold_chunks = int(self.silent_duration * self.rate / self.chunk)
        slient_threshold_rms=80
        silent_threshold_zcr=30
        #for _ in range(0, ):
        start_silence_check=0
        while True:
            data = stream.read(self.chunk)
            
            #Convert audio chunk to numpy array
           # frame= np.frombuffer(data, dtype=np.int16)
            #frame_rms=rms(frame)
            #frame_zcr=zero_crossing_rate(frame)
            #print(frame_rms, "RMS VALUE")
        #print(frame_zcr, "FRAME ZERO CROSSING RATE")
            #check for silent chuncks
            #if frame_rms< slient_threshold_rms and frame_zcr <silent_threshold_zcr:
             #   silent_chunks+=1
           # else:
            #    silent_chunks=0
            
            #if silence detected
            #print(start_silence_check, "Start slient check")
            if keyboard.is_pressed("q"): # Stop at silence didnt work. So we moving foward for now
                break
            frames.append(data)
            start_silence_check+=1
            
        #streaming ends here
        # Stop straming
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        
        # Save the recorded data
        with wave.open(self.wave_output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
            self.listened=True
        return 1
        #print(f"Audio saved as {self.wave_output_filename}")

    #transscibe audio to text
    def transcibe(self):
        text=""
        # Initialize recognizer
        recognizer = sr.Recognizer()
        # Open the audio file and transcribe
        if not self.listened:
            return 0, text
        with sr.AudioFile(self.wave_output_filename) as source:
            audio = recognizer.record(source)  # Read the audio file
            try:
                # Use Google Web Speech API for transcription
                text = recognizer.recognize_google(audio)
                #print("Transcribed Text: ", text)
            except sr.UnknownValueError:
                text= "Google Speech Recognition could not understand the audio"
            except sr.RequestError as e:
                text= f"Could not request results from Google Speech Recognition service; {e}"
        return 1, text
    #____________________text back to speech_________________
    def speak(self, txt):
        self.engine.say(txt)          # Convert text to speech
        self.engine.runAndWait()       # Wait for the speech to finish
        return 1
    
if __name__ == "__main__":
    speech= Speech() 
    print("Listening")
    if speech.listen():
        print("processing")
        cond, text = speech.transcibe()
        if cond==1:
            print(text)
        else:
            print("Something went wrong")
    print("test speaking")
    speech.speak("my name is Joseph")
    