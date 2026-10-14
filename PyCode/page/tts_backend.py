#!/usr/bin/env python3
"""Local backend that serves the HTML page and reuses the original TTS backend logic."""

from __future__ import annotations

import json
import mimetypes
import os
import re
import unicodedata
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent
os.chdir(str(BASE_DIR))

# Reuse the original TTS code so the voice generation matches the desktop app.
import eye_estonian_teacher_support as original_support


def normalize_cache_text(value: str) -> str:
    text = str(value or '')
    text = unicodedata.normalize('NFD', text)
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')
    text = text.lower()
    text = re.sub(r'[^a-zäöüõšž0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def generate_audio_file(text: str, lang: str, speaker: str = "mari", speed: float = 1.0, slow: bool = False) -> str:
    clean_text = (text or "").strip()
    if not clean_text:
        raise ValueError("No text provided for TTS generation.")

    canonical_text = normalize_cache_text(clean_text)
    if lang.lower() in {"et", "ee", "estonian"}:
        output_path = original_support._build_audio_cache_path(canonical_text, "tartunlp", "wav", speaker=speaker, api_speed=speed)
        if not os.path.exists(output_path):
            ok = original_support.estonian_tts_tartunlp(clean_text, speaker=speaker, api_speed=speed, output_filename=output_path)
            if not ok:
                raise RuntimeError(f"Estonian TTS failed for: {clean_text[:60]}")
        return output_path

    output_path = original_support._build_audio_cache_path(canonical_text, "gtts", "mp3", lang="en", api_speed=speed)
    if not os.path.exists(output_path):
        ok = original_support.english_tts_gtts(clean_text, lang="en", use_slow=slow, output_filename=output_path)
        if not ok:
            raise RuntimeError(f"English TTS failed for: {clean_text[:60]}")
    return output_path


def serialize_topics():
    topics_path = os.path.join(BASE_DIR, "topics.json")
    if not os.path.exists(topics_path):
        return {"topicList": [], "topicContent": {}}

    with open(topics_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    payload = {}
    for topic_name, entries in data.get("topicContent", {}).items():
        payload[topic_name] = [list(entry) for entry in entries]

    return {"topicList": data.get("topicList", []), "topicContent": payload}


class TTSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/topics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(serialize_topics()).encode("utf-8"))
            return

        if parsed.path == "/":
            self.path = "/eye_estonian_teacher.html"
        if parsed.path.startswith("/audio_cache/"):
            return super().do_GET()
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/tts":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length)
                payload = json.loads(body.decode("utf-8") or "{}")
                text = payload.get("text", "")
                lang = payload.get("lang", "et")
                speaker = payload.get("speaker", "mari")
                speed = float(payload.get("speed", 1.0))
                slow = bool(payload.get("slow", False))

                output_path = generate_audio_file(text, lang, speaker=speaker, speed=speed, slow=slow)
                relative_url = "/audio_cache/" + os.path.basename(output_path)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"url": relative_url, "path": output_path}).encode("utf-8"))
            except Exception as exc:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(exc)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not found")


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), TTSHandler)
    print(f"Serving app on http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
