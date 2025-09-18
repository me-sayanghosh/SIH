Running the backend (Windows PowerShell)

This backend scripts use local audio input, local Ollama LLM via langchain_ollama, Google STT (SpeechRecognition) and gTTS for TTS. Follow these steps.

1. Install Python 3.10+ (3.11 recommended) and ensure `python` is on PATH.

2. Create and activate a virtual environment (PowerShell):

```powershell
# from repository root (d:\SIH)
python -m venv .venv-backend; .\.venv-backend\Scripts\Activate.ps1
```

3. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
# Use pipwin for PyAudio if pip install fails
python -m pip install pipwin
python -m pip install -r Backend\requirements.txt || python -m pipwin install pyaudio
```

4. Install and run Ollama (local LLM):

- Ollama is not a Python package. Install from https://ollama.ai and follow OS instructions.
- Ensure a compatible model (e.g., llama3:8b) is installed in Ollama and Ollama is running ("ollama serve").

5. Microphone permissions:

- Make sure Windows allows microphone access for Python/Terminal.

6. Run the app:

```powershell
python Backend\main.py
```

7. Troubleshooting:

- PyAudio installation issues on Windows: use `python -m pipwin install pyaudio` or download prebuilt wheels.
- playsound on Windows sometimes interacts weirdly; if playback fails, try `pip install simpleaudio` and adapt `tts.py` to use `simpleaudio`.
- If Ollama fails, ensure `ollama` daemon is running and model name in `ollama_client.py` matches an installed model.
- If Google STT raises `RequestError`, it may be a network or quota issue.

8. Optional: If you prefer a conda environment, create one and install the same packages.

Contact me if you get specific errors and I'll guide next steps.
