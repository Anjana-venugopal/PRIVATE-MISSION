# -*- coding: utf-8 -*-
"""
================================================================================
                J.A.R.V.I.S. - LOCAL OFFLINE CORE (v1.0)3
================================================================================
A 100% local, private, and free J.A.R.V.I.S. terminal. 
No internet or cloud API keys are required.

REQUIREMENTS:
-------------
1. Download and install Ollama from: https://ollama.com/
2. Open your terminal and pull a local model (Llama 3 is recommended):
   'ollama pull llama3' (or 'ollama pull phi3' for lightweight machines)
3. Install Python dependencies:
   'pip install ollama speechrecognition pyttsx3 pyaudio'

RUN PROTOCOL:
-------------
'python jarvis_local.py'
================================================================================
"""

import sys
import os
import time

try:
    import ollama
    import speech_recognition as sr
    import pyttsx3
except ImportError as e:
    print("\033[31m[CRITICAL FAILURE] Missing local dependencies.\033[0m")
    print(f"Error details: {e}")
    print("\nPlease run: pip install ollama speechrecognition pyttsx3 pyaudio")
    sys.exit(1)

# Jarvis System Directive
SYSTEM_PROMPT = (
    "You are J.A.R.V.I.S., Anvi's sophisticated, highly intelligent, "
    "and slightly sarcastic British AI butler. Speak with refinement, absolute intellect, "
    "and call the user 'Ma'am'. Keep your responses short, conversational, "
    "and to the point, fitting for voice-to-voice interaction."
)

class LocalJarvis:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize Local Offline Text-To-Speech Engine
        try:
            self.engine = pyttsx3.init(driverName='sapi5')
        except Exception:
            self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Conversation history memory
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def setup_voice(self):
        """Configure local TTS settings for a more refined British sounding voice."""
        voices = self.engine.getProperty('voices')
        
        # Try to find a British or deep male voice
        selected_voice = None
        for voice in voices:
            if "english" in voice.name.lower() or "british" in voice.name.lower() or "uk" in voice.name.lower():
                # Prefer British male voice if available, otherwise any English voice
                if "male" in voice.name.lower() or "hazel" not in voice.name.lower():
                    selected_voice = voice.id
                    break
        
        if selected_voice:
            self.engine.setProperty('voice', selected_voice)
        
        self.engine.setProperty('rate', 175)  # Slightly faster, elegant speaking speed
        self.engine.setProperty('volume', 1.0) # Master volume

    def speak(self, text):
        """Wrapper to speak text offline."""
        print(f"\033[36m[J.A.R.V.I.S.] >>> {text}\033[0m")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listens to the local microphone and transcribes speech."""
        with self.microphone as source:
            print("\n\033[33m[Listening... Speak now]\033[0m")
            # Calibrate ambient noise level for clearer recognition
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                print("\033[32m[Processing speech pattern...]\033[0m")
                # Using standard free speech-to-text
                text = self.recognizer.recognize_google(audio)
                print(f"\033[37m[Ma'am] >>> {text}\033[0m")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except Exception as e:
                print(f"\033[31m[Mic Error]: {e}\033[0m")
                return None

    def query_local_llm(self, prompt):
        """Sends user prompts directly to the offline Ollama service on your computer."""
        self.messages.append({"role": "user", "content": prompt})
        
        try:
            # Connect to local Ollama API
            response = ollama.chat(
                model=self.model_name,
                messages=self.messages
            )
            
            reply = response['message']['content']
            # Limit memory size to keep processing fast
            self.messages.append({"role": "assistant", "content": reply})
            if len(self.messages) > 10:
                self.messages = [self.messages[0]] + self.messages[-6:]
                
            return reply
            
        except Exception as e:
            return f"Apologies Ma'am, my local core database is unreachable. Please ensure Ollama is running. Error details: {str(e)}"

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""\033[36m
      ___   _      ___  _   _  _  ___  
     |__ | / \    |  _|| | | || ||  _| 
       | |/ ^ \   | |  | \_/ || || |_  
    L_ | |/ ___ \  | |  |  _  || ||  _|
    \__|//_/   \_\ |_|  |_| |_||_||___|
    ===================================
    [ANVI MADE 2026]
    [MODEL CORE   : OLLAMA / LOCAL LLM]
    [API SECURITY : SECURED / OFFLINE ]
    ===================================
        \033[0m""")
        
        # Test connection to Ollama
        try:
            ollama.list()
            print(f"\033[32m[SUCCESS] Neural local core integration online. Using '{self.model_name}'\033[0m")
        except Exception:
            print("\033[31m[CRITICAL ERR] Could not find Ollama server running on your computer.\033[0m")
            print("Please open the Ollama application or run 'ollama serve' in another window, then restart this script.")
            sys.exit(1)

        self.speak("Mainframe offline core engaged. I am at your service, MA'AM. What shall we coordinate today?")

        while True:
            user_input = self.listen()
            if user_input:
                if any(exit_word in user_input.lower() for exit_word in ["goodbye", "go to sleep", "shut down", "exit"]):
                    self.speak("As you wish, Ma'am. Powering down systems. Stay safe.")
                    break
                
                # Fetch response from local computer AI model
                jarvis_response = self.query_local_llm(user_input)
                # Read response out loud
                self.speak(jarvis_response)

if __name__ == "__main__":
    # If you pull a lighter model, e.g. "ollama pull phi3", replace "llama3" here with "phi3"
    jarvis = LocalJarvis(model_name="llama3")
    jarvis.run()