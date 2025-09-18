import speech_recognition as sr

def record_and_transcribe(duration=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = r.listen(source, phrase_time_limit=duration)

    # Try Hindi first, fallback to English
    for lang in ["en-IN", "hi-IN"]:
        try:
            text = r.recognize_google(audio, language=lang)
            print(f"📝 Transcribed ({lang}):", text)
            return text
        except sr.UnknownValueError:
            continue  # try next language
        except sr.RequestError as e:
            print(f"⚠️ Could not request results; {e}")
            return ""

    print("⚠️ Google Speech could not understand audio in both Hindi and English")
    return ""
