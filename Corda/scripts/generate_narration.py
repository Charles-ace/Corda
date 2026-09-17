"""
Corda ElevenLabs Narration Generator
Reads Corda/docs/NARRATION.md, generates high-quality narration using ElevenLabs API,
saves to Corda/remotion/public/audio/narration.mp3, measures exact timing with ffprobe,
and updates Corda/docs/ACTUAL_AUDIO_TIMING.md and Corda/remotion/src/timing.ts.
"""

import os
import sys
import re
import json
import urllib.request
import subprocess

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NARRATION_PATH = os.path.join(BASE_DIR, "docs", "NARRATION.md")
VOICE_CONFIG_PATH = os.path.join(BASE_DIR, "remotion", "src", "voice.ts")
AUDIO_DIR = os.path.join(BASE_DIR, "remotion", "public", "audio")
AUDIO_OUTPUT_PATH = os.path.join(AUDIO_DIR, "narration.mp3")
ACTUAL_TIMING_PATH = os.path.join(BASE_DIR, "docs", "ACTUAL_AUDIO_TIMING.md")
TIMING_TS_PATH = os.path.join(BASE_DIR, "remotion", "src", "timing.ts")

def fetch_and_select_voice(api_key):
    """
    Queries ElevenLabs /v1/voices and selects a natural, professional English voice
    suitable for a tech startup / product demo.
    """
    print("Fetching available voices from ElevenLabs API...")
    url = "https://api.elevenlabs.io/v1/voices"
    req = urllib.request.Request(url, headers={"xi-api-key": api_key}, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"⚠️ ElevenLabs /v1/voices returned {e.code}: {err_msg}")
        print("API key has restricted 'voices_read' scope. Falling back to flagship ElevenLabs demo voice...")
        # Standard ElevenLabs premade voice: Adam (Deep, authoritative tech demo narrator)
        adam_voice_id = "pNInz6obpgDQGcFmaJgB"
        adam_voice_name = "Adam (Tech Narrator)"
        print(f"✓ Selected Flagship Voice: '{adam_voice_name}' (ID: {adam_voice_id})")
        return adam_voice_id, adam_voice_name
    except Exception as e:
        print(f"⚠️ Failed to query voices: {e}")
        adam_voice_id = "pNInz6obpgDQGcFmaJgB"
        adam_voice_name = "Adam (Tech Narrator)"
        print(f"✓ Selected Flagship Voice: '{adam_voice_name}' (ID: {adam_voice_id})")
        return adam_voice_id, adam_voice_name

    voices = data.get("voices", [])
    if not voices:
        print("❌ No voices returned from ElevenLabs API.")
        return None, None

    print(f"✓ Retrieved {len(voices)} available voices from ElevenLabs.")

    # Preferred voices ranked by natural authority and clarity for tech demo / oracle
    preferred_names = [
        "Adam", "Charlie", "George", "Callum", "Liam", "Will", "Eric", "Chris", "Daniel", "Brian", "Antoni", "Josh", "Rachel", "Drew"
    ]

    selected_voice = None
    # 1. First priority: Match against preferred curated list
    for p_name in preferred_names:
        for v in voices:
            if v.get("name", "").strip().lower() == p_name.lower():
                selected_voice = v
                break
        if selected_voice:
            break

    # 2. Second priority: Find any voice categorized with narration, news, presentation
    if not selected_voice:
        for v in voices:
            labels = v.get("labels") or {}
            desc = (v.get("description") or "").lower()
            use_case = (labels.get("use case") or labels.get("use_case") or "").lower()
            accent = (labels.get("accent") or "").lower()
            if any(term in use_case or term in desc for term in ["narration", "news", "presentation", "documentary"]):
                selected_voice = v
                break

    # 3. Third priority: First available English / premade voice
    if not selected_voice:
        selected_voice = voices[0]

    v_id = selected_voice.get("voice_id")
    v_name = selected_voice.get("name", "Unknown Voice")
    category = selected_voice.get("category", "")
    print(f"✓ Auto-selected Voice: '{v_name}' (Category: {category}, ID: {v_id})")
    return v_id, v_name

def save_voice_config(voice_id, voice_name=""):
    content = f"""// ElevenLabs Voice Configuration for Corda
export const VOICE_ID = "{voice_id}";
export const VOICE_NAME = "{voice_name}";
export const MODEL_ID = "eleven_multilingual_v2";
"""
    with open(VOICE_CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Saved voice configuration to: {VOICE_CONFIG_PATH}")

def get_voice_id():
    # 1. Environment variable priority
    if os.environ.get("ELEVENLABS_VOICE_ID"):
        return os.environ.get("ELEVENLABS_VOICE_ID")
    
    # 2. Check voice.ts
    if os.path.exists(VOICE_CONFIG_PATH):
        with open(VOICE_CONFIG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'export const VOICE_ID\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            val = match.group(1).strip()
            if val and val != "YOUR_CONFIGURED_VOICE_ID":
                return val
    return None

def get_model_id():
    if os.path.exists(VOICE_CONFIG_PATH):
        with open(VOICE_CONFIG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'export const MODEL_ID\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1).strip()
    return "eleven_multilingual_v2"

def main():
    print("==================================================")
    print("   CORDA — ElevenLabs Narration Pipeline")
    print("==================================================")

    # 1. Check API Key
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("\n❌ ELEVENLABS_API_KEY REQUIRED")
        print("Set the environment variable ELEVENLABS_API_KEY before running this script.")
        sys.exit(1)

    print(f"✓ ElevenLabs API Key: [DETECTED]")

    # 2. Check or Discover Voice ID
    voice_id = get_voice_id()
    if not voice_id or voice_id == "YOUR_CONFIGURED_VOICE_ID":
        print("Voice ID not explicitly configured. Discovering available voices via API...")
        voice_id, voice_name = fetch_and_select_voice(api_key)
        if not voice_id:
            print("❌ Unable to select a usable voice from ElevenLabs.")
            sys.exit(1)
        save_voice_config(voice_id, voice_name)
    else:
        print(f"✓ Using configured Voice ID: {voice_id}")

    model_id = get_model_id()
    print(f"✓ Model ID: {model_id}")

    # 3. Read Narration Text
    if not os.path.exists(NARRATION_PATH):
        print(f"❌ Narration file not found: {NARRATION_PATH}")
        sys.exit(1)

    with open(NARRATION_PATH, "r", encoding="utf-8") as f:
        narration_raw = f.read()

    # Parse beats from NARRATION.md (supports both 'BEAT 01' and 'BEAT_01')
    beats_raw = re.findall(r'###\s*(BEAT[_\s]?\d+:[^\n]+)\n(.*?)(?=\n###|\Z)', narration_raw, re.DOTALL)
    if not beats_raw:
        print("❌ Failed to parse beats from NARRATION.md")
        sys.exit(1)

    full_text_lines = []
    beat_texts = []
    for header, body in beats_raw:
        clean_body = " ".join(body.strip().split())
        # Normalize header and beat_id: e.g. "BEAT 01" -> "BEAT_01"
        header_clean = header.strip()
        beat_prefix = header_clean.split(":")[0].strip()
        normalized_id = re.sub(r'BEAT[_\s]?(\d+)', r'BEAT_\1', beat_prefix)
        normalized_title = f"{normalized_id}: {header_clean.split(':', 1)[1].strip()}"
        
        full_text_lines.append(clean_body)
        beat_texts.append((normalized_id, normalized_title, clean_body))

    full_narration = " ".join(full_text_lines)
    print(f"✓ Narration script loaded ({len(beat_texts)} beats, {len(full_narration.split())} words)")

    # 4. Generate via ElevenLabs API
    print("\nRequesting high-quality speech generation from ElevenLabs...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": full_narration,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    os.makedirs(AUDIO_DIR, exist_ok=True)

    try:
        with urllib.request.urlopen(req) as resp:
            audio_data = resp.read()
        with open(AUDIO_OUTPUT_PATH, "wb") as f:
            f.write(audio_data)
        print(f"✓ Saved narration audio to: {AUDIO_OUTPUT_PATH} ({len(audio_data)} bytes)")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"❌ ElevenLabs API Error ({e.code}): {err_msg}")
        sys.exit(1)

    # 5. Measure Actual Audio Duration with ffprobe
    print("\nMeasuring actual audio duration via ffprobe...")
    ffprobe_cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,sample_rate,format_name", "-of", "json", AUDIO_OUTPUT_PATH
    ]
    res = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("❌ ffprobe failed to measure audio duration:", res.stderr)
        sys.exit(1)

    probe_data = json.loads(res.stdout).get("format", {})
    duration = float(probe_data.get("duration", 0.0))
    sample_rate = probe_data.get("sample_rate", "44100")
    fmt_name = probe_data.get("format_name", "mp3")

    print(f"✓ Measured Duration: {duration:.2f} seconds")
    print(f"✓ Sample Rate: {sample_rate} Hz")
    print(f"✓ Format: {fmt_name}")

    # 6. Calculate Beat Boundaries proportionally based on words
    total_words = sum(len(body.split()) for _, _, body in beat_texts)
    current_time = 0.0
    beat_timings = []

    for beat_id, title, body in beat_texts:
        word_count = len(body.split())
        beat_duration = (word_count / total_words) * duration
        start = round(current_time, 2)
        end = round(current_time + beat_duration, 2)
        beat_timings.append({
            "id": beat_id,
            "title": title,
            "start": start,
            "end": end,
            "duration": round(end - start, 2),
            "text": body
        })
        current_time = end

    # Ensure last beat ends exactly at duration
    if beat_timings:
        beat_timings[-1]["end"] = round(duration, 2)
        beat_timings[-1]["duration"] = round(duration - beat_timings[-1]["start"], 2)

    # 7. Write Corda/docs/ACTUAL_AUDIO_TIMING.md
    timing_doc = f"""# Corda Actual Audio Timing

Audio file: `Corda/remotion/public/audio/narration.mp3`
Duration: {duration:.2f}s
Sample rate: {sample_rate} Hz
Format: {fmt_name}

"""
    for b in beat_timings:
        timing_doc += f"""### {b['title']}
Start: {b['start']}s
End: {b['end']}s
Duration: {b['duration']}s
Text: "{b['text']}"

"""

    with open(ACTUAL_TIMING_PATH, "w", encoding="utf-8") as f:
        f.write(timing_doc.strip() + "\n")
    print(f"✓ Generated: {ACTUAL_TIMING_PATH}")

    beats_json = json.dumps(beat_timings, indent=2)
    timing_ts = f"""// Generated by Corda Narration Pipeline
export type Beat = {{
  id: string;
  start: number; // in seconds
  end: number;   // in seconds
  duration: number; // in seconds
  title: string;
  text: string;
}};

export const TOTAL_DURATION_SECONDS = {duration:.2f};
export const FPS = 30;
export const TOTAL_DURATION_FRAMES = Math.ceil(TOTAL_DURATION_SECONDS * FPS);

export const beats: Beat[] = {beats_json};
"""
    with open(TIMING_TS_PATH, "w", encoding="utf-8") as f:
        f.write(timing_ts.strip() + "\n")
    print(f"✓ Updated: {TIMING_TS_PATH}")

    print("\n✨ Audio Generation & Precise Timing Complete!")

if __name__ == "__main__":
    main()
