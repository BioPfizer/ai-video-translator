# AI Video Translator

AI-powered video translation system that automatically transcribes, translates, and dubs videos between any language.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

## Features

- Automatic speech-to-text transcription (Whisper)
- Translation between any worldwide language.
- AI-generated voice dubbing (Edge-TTS)
- Drag-and-drop video upload
- Real-time processing status
- Modern animated UI

## Tech Stack

**Backend:**
- FastAPI
- OpenAI Whisper (Speech-to-Text)
- DeepL/Google Translate API
- Edge-TTS (Text-to-Speech)
- FFmpeg (Video processing)

**Frontend:**
- Next.js 14
- TypeScript
- Tailwind CSS
- shadcn/ui + Aceternity UI
- Framer Motion

## How It Works

1. Upload video or paste URL (YouTube, TikTok, Instagram)
2. Select source and target languages
3. System extracts audio and transcribes speech
4. Translates text to target language
5. Generates new audio with AI voice
6. Merges audio back into video
7. Download translated video

## Local Development

### Backend Setup

```bash
cd video-translator-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd video-translator-frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## Deployment

- **Backend**: Railway
- **Frontend**: Vercel

See individual README files in each directory for deployment instructions.

## Project Structure

```
ai-video-translator/
├── video-translator-api/      # FastAPI backend
│   ├── app/
│   │   ├── models/            # Pydantic schemas
│   │   ├── services/          # Core services (STT, TTS, Translation)
│   │   └── utils/             # File handling utilities
│   └── main.py
├── video-translator-frontend/  # Next.js frontend
│   ├── app/
│   ├── components/
│   └── public/
└── assets/                     # Project assets
```

## API Endpoints

- `POST /api/translate` - Translate text
- `POST /api/tts` - Text-to-speech
- `POST /api/stt` - Speech-to-text
- `POST /api/translate-video` - Full video translation pipeline

## License

MIT License - see LICENSE file for details

## Future Enhancements

- Support for more languages
- Batch video processing
- Video subtitle generation
- Voice cloning options
- Real-time streaming translation
