from gtts import gTTS
import tempfile, os, platform, subprocess


def _play_with_playsound(path):
    try:
        from playsound import playsound
        playsound(path)
        return True
    except Exception:
        return False


def _play_fallback(path):
    system = platform.system()
    try:
        if system == 'Windows':
            # os.startfile will open the mp3 with the default player
            os.startfile(path)
            return True
        elif system == 'Darwin':
            subprocess.run(['afplay', path], check=True)
            return True
        else:
            # Try common Linux players
            for cmd in (['mpg123', path], ['mpv', path], ['mplayer', path]):
                try:
                    subprocess.run(cmd, check=True)
                    return True
                except Exception:
                    continue
    except Exception:
        pass
    return False


def speak_text(text, lang="en"):
    """Converts text to speech using gTTS and plays it.

    This function tries to use `playsound` first. If `playsound` is not
    available or fails, it falls back to a platform-specific playback
    method (Windows: os.startfile, macOS: afplay, Linux: mpg123/mpv/mplayer).

    Only 'hi' and 'en' are supported by this code path.
    """
    if not text:
        print("⚠️ No text to speak.")
        return

    lang = "hi" if lang == "hi" else "en"

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)
            filename = fp.name

        # Try playsound first, then fallback
        if _play_with_playsound(filename):
            pass
        elif _play_fallback(filename):
            pass
        else:
            print("⚠️ No audio player found. Please install 'playsound' or 'mpg123/mpv/mplayer' on your system.")

    except Exception as e:
        print(f"❌ TTS error: {e}")
    finally:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except Exception:
            pass
