#THIS PY PROGRAM TRANSLATOR MODEL IS FOR ONLINE USE ONLY 
#TO USE ONLINE AND OFFLINE MODELS BOTH CHOOSE THE cglang_on_off.py FILE


import speech_recognition as sr
from gtts import gTTS
import os
import json
from openai import OpenAI
from playsound import playsound
import time

client = OpenAI(api_key=os.getenv("OPENAI_AP_KEY"))

with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

def save_translation(english, chhattisgarhi):
    translations[english.lower()] = (chhattisgarhi, "")
    with open("translations.json", "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=4)



def save_new_translation(english_text, chhattisgarhi_text):
    translations[english_text.lower()] = (chhattisgarhi_text, "")
    with open("translations.json", "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=4)
    print("...translation saved for next time.")

def get_ai_translation(sentence):
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

def translate(sentence):
    sentence_lower = sentence.strip().lower()

    if sentence_lower in translations:
        print("...found in local file.")
        return translations[sentence_lower][0]
    
    else:
        result = get_ai_translation(sentence)
        if "AI error" not in result:
            save_new_translation(sentence, result)
        return result

def speak(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("audio.mp3")
    
    playsound("audio.mp3")
    
    time.sleep(1) 
    os.remove("audio.mp3")



r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("\nSpeak something (or say 'exit' to stop)...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        user_text = r.recognize_google(audio, language="en-IN")
        print(f"You said: {user_text}")

        if user_text.lower() == 'exit':
            print("Goodbye!")
            break
        
        chhattisgarhi_translation = translate(user_text)
        print(f"Chhattisgarhi: {chhattisgarhi_translation}")

        if "error" not in chhattisgarhi_translation.lower():
            speak(chhattisgarhi_translation)
            
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
    except sr.RequestError:
        print("Could not connect to the speech service.")