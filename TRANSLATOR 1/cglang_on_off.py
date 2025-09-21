#THIS PY PROGRAM TRANSLATOR MODEL IS FOR ONLINE AND OFFLINE BOTH 
#TO USE ONLY ONLINE MODEL CHOOSE THE cglang_online.py FILE
#TO DEPLOY OPENAI API --->setx OPENAI_API_KEY "your_api_key" {better create a new api key for it}



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

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

offline_tts_model = None
offline_tts_tokenizer = None
try:
    print("Loading offline TTS model... (this may take a moment the first time)")
    offline_tts_model = VitsModel.from_pretrained("facebook/mms-tts-hin")
    offline_tts_tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-hin")
    print("...Offline TTS model loaded successfully.")
except Exception as e:
    print(f"FATAL: Could not load the offline TTS model: {e}")
    print("Please ensure you have an internet connection the first time you run this to download the model.")

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        print("...Internet connection found.")
        return True
    except (requests.ConnectionError, requests.Timeout):
        print("...No internet connection detected.")
        return False

def save_new_translation(english_text, chhattisgarhi_text):
    translations[english_text.lower()] = (chhattisgarhi_text, "")
    with open("translations.json", "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=4)
    print("...translation saved for next time.")

def get_ai_translation(sentence):
    if not client:
        return "AI error: OpenAI client not initialized."
    print("...not in dictionary, asking AI.")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a translator. Translate the user's text to Chhattisgarhi. Only give the translation, nothing else."},
                {"role": "user", "content": sentence}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI error: {e}"

def translate(sentence, is_online):
    sentence_lower = sentence.strip().lower()

    if sentence_lower in translations:
        print("...found in local file.")
        return translations[sentence_lower][0]
    
    elif is_online:
        result = get_ai_translation(sentence)
        if "AI error" not in result:
            save_new_translation(sentence, result)
        return result
    else:
        return "Translation not found in the local dictionary. Offline mode is active."

def speak_online(text):
    try:
        tts = gTTS(text=text, lang='hi')
        tts.save("audio.mp3")
        playsound("audio.mp3")
        time.sleep(1)
        os.remove("audio.mp3")
    except Exception as e:
        print(f"Error with online speech: {e}")

def speak_offline(text):
    """Generates speech using the local AI model."""
    if not offline_tts_model or not offline_tts_tokenizer:
        print("Offline TTS model not available.")
        return

    try:
        print("...generating speech with local AI.")
        inputs = offline_tts_tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = offline_tts_model(**inputs).waveform

        temp_audio_file = "offline_speech.wav"
        sf.write(temp_audio_file, output.squeeze().cpu().numpy(), samplerate=16000)
        
        playsound(temp_audio_file, block=True)
        os.remove(temp_audio_file) # Clean up the file

    except Exception as e:
        print(f"Error during offline speech generation: {e}")

def run_online_mode():
    print("\n--- ONLINE MODE ACTIVATED ---")
    print("Speech-to-speech translation is ready.")
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("\nSpeak something (or say 'exit' to stop)...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("Listening timed out. Please try speaking again.")
                continue

        try:
            user_text = r.recognize_google(audio, language="en-IN")
            print(f"You said: {user_text}")

            if user_text.lower() == 'exit':
                break
            
            chhattisgarhi_translation = translate(user_text, is_online=True)
            print(f"Chhattisgarhi: {chhattisgarhi_translation}")

            if "error" not in chhattisgarhi_translation.lower():
                speak_online(chhattisgarhi_translation)
                
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError:
            print("Could not connect to the speech service. Check your internet.")

def run_offline_mode():
    print("\n--- OFFLINE MODE ACTIVATED ---")
    print("Only translations from the local dictionary are available.")
    while True:
        user_text = input("\nEnter English text to translate (or 'exit' to stop): ")
        
        if user_text.lower() == 'exit':
            break

        chhattisgarhi_translation = translate(user_text, is_online=False)
        print(f"Chhattisgarhi: {chhattisgarhi_translation}")
        
        if "not found" not in chhattisgarhi_translation:
            speak_offline(chhattisgarhi_translation)

if __name__ == "__main__":
    if check_internet():
        run_online_mode()
    else:
        run_offline_mode()
    

    print("\nGoodbye!")
