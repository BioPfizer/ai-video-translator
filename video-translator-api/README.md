# Video Translator API

FastAPI backend for AI video translation.

## Tech Stack

- FastAPI
- OpenAI Whisper (base model)
- Google Translate (deep-translator)
- Edge-TTS (Microsoft voices)
- FFmpeg (video/audio processing)

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`

API docs: `http://localhost:8000/docs`

## Environment Variables

Currently no API keys required. All services use free tiers:
- Whisper (local model)
- Google Translate (free API via deep-translator)
- Edge-TTS (free Microsoft service)

## Deployment to Railway

1. Push code to GitHub
2. Create new project on Railway
3. Connect GitHub repository
4. Railway will auto-detect Python and deploy
5. Add environment variables (if any)
6. Deploy

**Note**: Railway may need to install system dependencies:
```
apt-get install ffmpeg
```

Add this to `nixpacks.toml` if needed.

## API Endpoints

### Health Check
```
GET /
GET /health
```

### Text Translation
```
POST /api/translate
Content-Type: application/json

{
  "text": "Hello world",
  "source_lang": "en",
  "target_lang": "zh-CN"
}
```

### Text-to-Speech
```
POST /api/tts
Content-Type: application/json

{
  "text": "Hello world",
  "language": "en"
}
```

### Speech-to-Text
```
POST /api/stt
Content-Type: multipart/form-data

file: audio.mp3
```

### Video Translation (Full Pipeline)
```
POST /api/translate-video
Content-Type: multipart/form-data

file: video.mp4
source_lang: en
target_lang: zh-CN
```

## Supported Languages

- `en` - English
- `zh-CN` - Chinese (Mandarin)
- `ms` - Malay

## Project Structure

```
video-translator-api/
├── app/
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── services/
│   │   ├── stt_service.py      # Whisper transcription
│   │   ├── translation_service.py  # Google Translate
│   │   ├── tts_service.py      # Edge-TTS
│   │   └── video_service.py    # FFmpeg operations
│   ├── utils/
│   │   └── file_handler.py     # File upload/cleanup
│   └── main.py                 # FastAPI app
├── uploads/                    # Temporary uploads
├── outputs/                    # Generated files
└── requirements.txt
```

## Notes

- Whisper "base" model loads on first transcription (takes ~10s)
- Temporary files are auto-cleaned after processing
- Max video size: 100MB (configurable)
- Processing time: ~30-60 seconds per video
