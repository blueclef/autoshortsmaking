import os
import requests
import subprocess

# IMPORTANT: Set your Gemini API key in your environment variables.
GEMINI_API_KEY = os.getenv('AIzaSyBDkxp4iGNtcZ8ri6Ezp34BxamvKjbCjbA')
GEMINI_TTS_ENDPOINT = 'https://api.generativeai.googleapis.com/v1/text:speech'  # Example endpoint

def synthesize_tts(text: str, out_file: str, duration: float = 30.0) -> None:
    """
    Synthesizes speech from text or creates a silent audio file if the API key is missing.
    """
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not set. Creating a silent placeholder audio file.")
        create_silent_audio(out_file, duration)
        return

    payload = {
        'input': {'text': text},
        'voice': {'languageCode': 'ko-KR', 'name': 'ko-KR-Standard-A'}, # Example voice
        'audioConfig': {'audioEncoding': 'MP3'}
    }
    headers = {'Authorization': f'Bearer {GEMINI_API_KEY}'}

    try:
        response = requests.post(GEMINI_TTS_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        with open(out_file, 'wb') as f:
            f.write(response.content)
        print(f"TTS audio saved to {out_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini TTS API: {e}. Creating silent placeholder.")
        create_silent_audio(out_file, duration)

def create_silent_audio(out_file: str, duration: float):
    """Creates a silent MP3 audio file for the given duration using FFmpeg."""
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi',
        '-i', f'anullsrc=r=44100:cl=mono',
        '-t', str(duration),
        '-q:a', '9',
        '-acodec', 'libmp3lame',
        out_file
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Created silent placeholder audio at {out_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create silent audio with FFmpeg: {e.stderr}")
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not in the system's PATH.")
