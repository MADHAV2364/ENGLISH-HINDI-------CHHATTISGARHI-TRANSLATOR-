📍📍📍 VERY IMPORTANT 📍📍📍 
TO DEPLOY OPENAI API --->setx OPENAI_API_KEY "your_api_key" {better create a new api key for it}


# 🗣️ English to Chhattisgarhi Speech Translator

A smart, dual-mode voice and text translator built in Python. This application provides real-time, speech-to-speech translation when online and intelligently falls back to a text-to-speech mode using a local dictionary when offline.

---

## ## Key Features ✨

* **🌐 Dual-Mode Operation**: Automatically detects internet connectivity and switches between two modes:
    * **Online Mode**: Full-featured, real-time, speech-to-speech translation.
    * **Offline Mode**: Text-to-speech translation using locally saved phrases.
* **🧠 AI-Powered Translation**: Leverages the OpenAI API (`gpt-4o-mini`) for accurate and context-aware translations in online mode.
* **💾 Smart Caching**: Every new translation fetched online is saved to a local `translations.json` file, expanding the translator's offline capabilities over time.
* **🔊 High-Quality Voice Synthesis**:
    * Uses Google Text-to-Speech (`gTTS`) for natural-sounding voices online.
    * Employs a cutting-edge, offline AI model from Hugging Face (`transformers`) for high-quality speech synthesis without an internet connection.
* **💪 Robust and Reliable**: Built with robust audio playback libraries (`sounddevice`, `pydub`) to avoid common errors and ensure smooth operation, especially on Windows.

---

## ## How It Works ⚙️

The application starts by checking for an internet connection to determine the operating mode.

### ### Online Mode (Internet Detected)

1.  **Listen**: The microphone listens for English speech using the `speech_recognition` library.
2.  **Transcribe**: The speech is converted to text using Google's Web Speech API.
3.  **Translate**: The English text is sent to the OpenAI API, which returns the translation in Chhattisgarhi.
4.  **Cache**: The new translation pair is saved to `translations.json`.
5.  **Speak**: The Chhattisgarhi text is converted to high-quality audio using `gTTS` and played back.

### ### Offline Mode (No Internet)

1.  **Input**: The user types English text into the console.
2.  **Lookup**: The program searches for the text in the `translations.json` file.
3.  **Translate**: If found, it retrieves the corresponding Chhattisgarhi text.
4.  **Speak**: The Chhattisgarhi text is synthesized into audio locally using the Hugging Face `transformers` AI model and played back through the speakers.

---

## ## Technology Stack 🛠️

* **Core Language**: Python 3
* **AI & Translation**: OpenAI API, Hugging Face `transformers`
* **Speech Recognition**: `SpeechRecognition` (using Google Web Speech API)
* **Text-to-Speech (TTS)**: `gTTS` (online), `transformers` (offline)
* **Audio Handling**: `sounddevice`, `pydub`, `soundfile`
* **Core AI Library**: `torch` (PyTorch)

---

Core Requirements and Library:-
import speech_recognition as sr
from gtts import gTTS
import os
import json
from openai import OpenAI
from playsound import playsound
import time
import requests
from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf

