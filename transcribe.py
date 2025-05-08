from fastapi import APIRouter, UploadFile, File
import shutil
import os
import wave
import subprocess
from vosk import Model, KaldiRecognizer
import json

router = APIRouter()

import os

# Path to Vosk Hindi model - user must download and extract the model here
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "vosk-model-small-hi-0.22")

# Load model once
if not os.path.exists(VOSK_MODEL_PATH):
    raise RuntimeError(f"Vosk model not found at {VOSK_MODEL_PATH}. Please download and extract the model.")

model = Model(VOSK_MODEL_PATH)

import os
import shutil
import wave
import subprocess
from fastapi import APIRouter, UploadFile, File, HTTPException
from vosk import Model, KaldiRecognizer
import json

router = APIRouter()

# Path to Vosk Hindi model - user must download and extract the model here
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "vosk-model-small-hi-0.22")

# Load model once
if not os.path.exists(VOSK_MODEL_PATH):
    raise RuntimeError(f"Vosk model not found at {VOSK_MODEL_PATH}. Please download and extract the model.")

model = Model(VOSK_MODEL_PATH)

import os

import logging
import os
import shutil
import subprocess
import wave
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from vosk import Model, KaldiRecognizer

router = APIRouter()

# Path to Vosk Hindi model - user must download and extract the model here
VOSK_MODEL_PATH = os.path.join(os.path.dirname(__file__), "vosk-model-small-hi-0.22")

# Load model once
if not os.path.exists(VOSK_MODEL_PATH):
    raise RuntimeError(f"Vosk model not found at {VOSK_MODEL_PATH}. Please download and extract the model.")

model = Model(VOSK_MODEL_PATH)

# Setup logger
logger = logging.getLogger("transcribe")
logging.basicConfig(level=logging.INFO)

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

# On Windows, if FFMPEG_PATH is just "ffmpeg", replace with full path to ffmpeg.exe
if os.name == "nt" and FFMPEG_PATH == "ffmpeg":
    # Try to find ffmpeg.exe in common locations or environment PATH
    import shutil
    ffmpeg_full_path = shutil.which("ffmpeg.exe")
    if ffmpeg_full_path:
        FFMPEG_PATH = ffmpeg_full_path

@router.post("/upload")
async def transcribe_audio(file: UploadFile = File(...)):
    import traceback
    temp_dir = os.path.join(os.path.dirname(__file__), "temp_audio")
    os.makedirs(temp_dir, exist_ok=True)
    temp_audio_path = os.path.join(temp_dir, file.filename)
    temp_wav_path = os.path.join(temp_dir, f"{file.filename}.wav")
    temp_text_path = os.path.join(temp_dir, f"{file.filename}.txt")

    try:
        logger.info(f"Using ffmpeg path: {FFMPEG_PATH}")
        # Save uploaded file
        with open(temp_audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert audio to wav mono 16kHz using ffmpeg
        command = [
            FFMPEG_PATH,
            "-y",
            "-i", temp_audio_path,
            "-ar", "16000",
            "-ac", "1",
            "-f", "wav",
            temp_wav_path
        ]
        logger.info(f"Running ffmpeg command: {' '.join(command)}")
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Open wav file for transcription
        wf = wave.open(temp_wav_path, "rb")

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                results.append(res.get("text", ""))
        # Final partial result
        res = json.loads(rec.FinalResult())
        results.append(res.get("text", ""))

        transcription_text = " ".join(results).strip()

        # Wrap transcription text in formatted document style
        formatted_text = f"""मध्य प्रदेश शासन
कार्यालय कलेक्टर एवं जिला दण्डाधिकारी
जिला – ग्वालियर, मध्य प्रदेश
फोन: 0751-1234567 | ईमेल: collector.gwalior@mp.gov.in | वेबसाइट: www.gwalior.mp.gov.in
________________________________________
आदेश
क्रमांक: 1234/स्थापना/2025
ग्वालियर, दिनांक: 29/04/2025
________________________________________
विषय: राज्यपाल राज्य के स्न असभ्य बौने प्रमुख और केंद्र।
________________________________________

{transcription_text}

________________________________________
(हस्ताक्षर)
[श्रीमान कलेक्टर का नाम]
कलेक्टर एवं जिला दण्डाधिकारी
ग्वालियर, मध्य प्रदेश
________________________________________
प्रतिलिपि:
1.	संबंधित अधिकारी – जानकारी हेतु।
2.	कार्यालय प्रति – सुरक्षित रखने हेतु।
3.	समस्त विभागाध्यक्ष – आवश्यक कार्यवाही हेतु।
"""

        # Save formatted transcription to text file
        with open(temp_text_path, "w", encoding="utf-8") as f:
            f.write(formatted_text)

        # Return formatted transcription text and download URL (adjust static serving as needed)
        return {
            "text": formatted_text,
            "download_url": f"/temp_audio/{file.filename}.txt"
        }
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"Error during transcription: {tb}")
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
