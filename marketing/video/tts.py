"""Free neural voice for the videos. One WAV per line, 24 kHz mono.
Each voice has a preferred engine and a fallback: Microsoft Edge neural voices (online) or
Kokoro (open model, runs offline); silence only for local previews without any voice.
Voices can be tuned: rate (+% faster) and pitch (Hz) for Edge, speed for Kokoro."""
import asyncio, os, pathlib, subprocess, wave

KOKORO_DIR = pathlib.Path(os.environ.get("KOKORO_DIR", pathlib.Path.home() / ".cache" / "kokoro"))
VOICES = {
    # name: engine order, Edge voice + tuning, Kokoro voice + speed
    "warm":    {"order": ["kokoro", "edge"], "edge": "en-US-AvaMultilingualNeural", "kokoro": "af_heart"},
    "calm":    {"order": ["kokoro", "edge"], "edge": "en-US-AndrewMultilingualNeural", "kokoro": "am_michael"},
    # the channel voice (chosen: Andrew, louder and livelier) and candidates in the same family
    "andrew_up":      {"order": ["edge", "kokoro"], "edge": "en-US-AndrewMultilingualNeural", "rate": 10, "pitch": 4, "kokoro": "am_michael", "speed": 1.1},
    "andrew_up2":     {"order": ["edge", "kokoro"], "edge": "en-US-AndrewMultilingualNeural", "rate": 16, "pitch": 8, "kokoro": "am_michael", "speed": 1.15},
    "brian_up":       {"order": ["edge", "kokoro"], "edge": "en-US-BrianMultilingualNeural", "rate": 10, "pitch": 4, "kokoro": "am_michael", "speed": 1.1},
    "guy_up":         {"order": ["edge", "kokoro"], "edge": "en-US-GuyNeural", "rate": 8, "pitch": 2, "kokoro": "am_michael", "speed": 1.1},
}
RATE = 24000


def _to_wav24k(src, dst):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(RATE), "-sample_fmt", "s16", str(dst)], check=True)


def _kokoro(text, voice, dst, speed):
    from kokoro_onnx import Kokoro
    import soundfile as sf
    if not hasattr(_kokoro, "k"):
        _kokoro.k = Kokoro(str(KOKORO_DIR / "kokoro-v1.0.onnx"), str(KOKORO_DIR / "voices-v1.0.bin"))
    samples, sr = _kokoro.k.create(text, voice=voice, speed=speed, lang="en-us")
    tmp = dst.with_suffix(".raw.wav"); sf.write(tmp, samples, sr); _to_wav24k(tmp, dst); tmp.unlink()


def _edge(text, voice, dst, rate, pitch):
    import edge_tts
    tmp = dst.with_suffix(".mp3")
    asyncio.run(edge_tts.Communicate(text, voice, rate=f"{rate:+d}%", pitch=f"{pitch:+d}Hz").save(str(tmp)))
    _to_wav24k(tmp, dst); tmp.unlink()


def _silence(text, dst):
    secs = max(0.8, len(text.split()) / 2.6)
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(b"\0\0" * int(secs * RATE))


def duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def speak(text, dst, voice="andrew_up", speed=None, engine=None):
    """Writes dst (wav) and returns the engine used. `speed` (e.g. 1.1) overrides the voice's own pace."""
    dst = pathlib.Path(dst)
    v = VOICES.get(voice, VOICES["andrew_up"])
    order = [engine] if engine else v["order"] + ["silence"]
    errors = []
    for e in order:
        try:
            if e == "kokoro":
                _kokoro(text, v["kokoro"], dst, speed or v.get("speed", 1.0))
            elif e == "edge":
                rate = round((speed - 1) * 100) if speed else v.get("rate", 0)
                _edge(text, v["edge"], dst, rate, v.get("pitch", 0))
            elif e == "silence":
                _silence(text, dst)
            return e
        except Exception as ex:  # try the next engine
            errors.append(f"{e}: {ex}")
    raise RuntimeError("; ".join(errors))
