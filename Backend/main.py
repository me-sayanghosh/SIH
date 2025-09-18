from stt_google import record_and_transcribe
from ollama_client import query_ollama, detect_language
from tts import speak_text

def main():
    user_text = record_and_transcribe()
    reply, lang = query_ollama(user_text)
    print("\n===== Ollama Reply =====")
    print(reply)

    speak_text(reply, lang=lang)  # speaks only in English or Hindi


if __name__ == "__main__":
    main()