"""
Corda End-to-End Demo Video Pipeline Orchestrator
Executes:
1. generate_narration.py (ElevenLabs TTS + ffprobe measurement + timing.ts update)
2. render_video.py (Remotion render + video ffprobe QA + completion report)
"""

import os
import sys
import subprocess

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = sys.executable

def main():
    print("\n==================================================")
    print("   CORDA — END-TO-END DEMO VIDEO PIPELINE")
    print("==================================================\n")

    # Step 1: Generate Narration
    gen_script = os.path.join(BASE_DIR, "scripts", "generate_narration.py")
    res1 = subprocess.run([PYTHON_EXE, gen_script])
    if res1.returncode != 0:
        sys.exit(res1.returncode)

    # Step 2: Render Video & QA
    render_script = os.path.join(BASE_DIR, "scripts", "render_video.py")
    res2 = subprocess.run([PYTHON_EXE, render_script])
    if res2.returncode != 0:
        sys.exit(res2.returncode)

if __name__ == "__main__":
    main()
