from flask import Flask, jsonify, request
from flask_cors import CORS

# Import local backend helpers
try:
    from ollama_client import query_ollama
except Exception:
    # If imports fail (dependencies not installed) we'll handle at runtime with clear errors
    query_ollama = None

import base64
import tempfile
import os
from gtts import gTTS


def synthesize_base64_mp3(text, lang='en'):
    """Synthesize speech to an MP3 and return base64-encoded bytes."""
    # Force only 'hi' or 'en'
    lang = 'hi' if lang == 'hi' else 'en'
    fd, path = tempfile.mkstemp(suffix='.mp3')
    os.close(fd)
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(path)
        with open(path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode('ascii')
    finally:
        try:
            os.remove(path)
        except Exception:
            pass

app = Flask(__name__)
CORS(app)


@app.route("/")
def index_root():
    return (
        "<html><body><h2>CropWise backend is running</h2>"
        "<p>Available endpoints: /api/ping (GET), /api/ask (POST), /api/translate (POST)</p>"
        "</body></html>",
        200,
    )


@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok", "message": "pong from backend"})


@app.route("/api/translate", methods=["POST"])
def translate():
    """
    Placeholder translate endpoint. Expects JSON: { text: str, target: 'en'|'hi' }
    For now this simply echoes input; replace with Google Translate / other logic later.
    """
    data = request.get_json() or {}
    text = data.get("text", "")
    target = data.get("target", "en")
    # echo back for now
    return jsonify({"translatedText": text, "target": target})



@app.route("/api/ask", methods=["POST"])
def ask():
    """
    Accepts JSON { text: string } and returns { reply: string, lang: 'en'|'hi' }
    Uses local ollama via `ollama_client.query_ollama`.
    """
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "no text provided"}), 400

    if query_ollama is None:
        return jsonify({"error": "backend dependency not available: ollama_client not importable"}), 500

    try:
        reply, lang = query_ollama(text)
        result = {"reply": reply, "lang": lang}
        # If client requested TTS, synthesize and include base64 MP3
        if data.get('speak'):
            try:
                b64 = synthesize_base64_mp3(reply, lang=lang)
                result['audio_base64'] = b64
            except Exception as e:
                result['audio_error'] = str(e)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Print a list of registered routes to help debug 'Not Found' issues
    try:
        print("Registered routes:")
        for rule in app.url_map.iter_rules():
            print(f"{rule.methods} -> {rule}")
    except Exception:
        pass
    app.run(host="0.0.0.0", port=5001, debug=True)
