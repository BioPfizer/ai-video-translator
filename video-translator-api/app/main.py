from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from dotenv import load_dotenv

from app.models.schemas import (
    TranslationRequest, 
    TranslationResponse,
    TTSRequest,
    STTResponse,
    LanguageCode
)

from app.services.stt_service import STTService
from app.services.translation_service import TranslationService
from app.services.tts_service import TTSService
from app.services.video_service import VideoService
from app.utils.file_handler import FileHandler

# Load environment variables
load_dotenv

# Initialize FastAPI app
app = FastAPI(
    title = "Elvet Video Translator API",
    description = "Translate reels between any language.",
    version = "1.0.0"
)

# CORS middleware (allow frontend connections)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (lazy loading on first use)
stt_service = None
translation_service = None
tts_service = None
video_service = VideoService()
file_handler = FileHandler()

def get_stt_service():
    """Lazy load STT service (Whisper model is large)"""
    global stt_service
    if stt_service is None:
        stt_service = STTService(model_size="base")
    return stt_service

def get_translation_service():
    """Lazy load translation service"""
    global translation_service
    if translation_service is None:
        translation_service = TranslationService()
    return translation_service

def get_tts_service():
    """Lazy load TTS service"""
    global tts_service
    if tts_service is None:
        tts_service = TTSService()
    return tts_service


################ HEALTH CHECK ################
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Elvet Video Translator API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "translate_text": "/api/translate",
            "text_to_speech": "/api/tts",
            "speech_to_text": "/api/stt",
            "translate_video": "/api/translate-video"
        }
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "stt": "ready" if stt_service else "not_loaded",
            "translation": "ready" if translation_service else "not_loaded",
            "tts": "ready" if tts_service else "not_loaded",
            "video": "ready"
        }
    }


################ TEXT TRANSLATION ################
@app.post("/api/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text between languages
    
    Example:
```json
    {
        "text": "Hello world",
        "source_lang": "en",
        "target_lang": "zh-CN"
    }
```
    """
    try:
        translator = get_translation_service()
        
        translated = translator.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return TranslationResponse(
            original_text=request.text,
            translated_text=translated,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


################ TEXT-TO-SPEECH ################
@app.post("/api/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech audio file
    
    Returns audio file download
    """
    try:
        tts = get_tts_service()
        
        # Generate output path
        output_path = file_handler.get_output_path("tts", ".mp3")
        
        # Generate speech
        audio_file = await tts.generate_speech_async(
            text=request.text,
            language=request.language.value,
            output_path=output_path
        )
        
        return FileResponse(
            audio_file,
            media_type="audio/mpeg",
            filename=Path(audio_file).name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


################ SPEECH-TO-TEXT ################
@app.post("/api/stt", response_model=STTResponse)
async def speech_to_text(file: UploadFile = File(...)):
    """
    Transcribe audio/video file to text
    
    Accepts: mp3, wav, mp4, avi, mov
    """
    try:
        # Save uploaded file
        temp_file = file_handler.save_upload(file, prefix="audio")
        
        # Transcribe
        stt = get_stt_service()
        text, detected_lang = stt.transcribe(temp_file)
        
        # Get duration (if video, extract audio first)
        try:
            duration = video_service.get_video_duration(temp_file)
        except:
            duration = 0.0
        
        # Cleanup
        file_handler.cleanup_file(temp_file)
        
        return STTResponse(
            text=text,
            language=detected_lang,
            duration=duration
        )
        
    except Exception as e:
        # Cleanup on error
        if 'temp_file' in locals():
            file_handler.cleanup_file(temp_file)
        raise HTTPException(status_code=500, detail=str(e))


################ VIDEO TRANSLATION (FULL PIPELINE) ################
@app.post("/api/translate-video")
async def translate_video(
    file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...)
):
    """
    Full pipeline: Video → Transcribe → Translate → TTS → New Video
    
    Form Data:
    - file: Video file (mp4, avi, mov)
    - source_lang: Source language (en, zh-CN, ms)
    - target_lang: Target language (en, zh-CN, ms)
    
    Returns: Translated video file
    """
    temp_files = []
    
    try:
        print("\n" + "="*60)
        print("VIDEO TRANSLATION PIPELINE")
        print("="*60)
        
        # Validate languages
        if source_lang not in ["en", "zh-CN", "ms"]:
            raise HTTPException(400, "Invalid source language")
        if target_lang not in ["en", "zh-CN", "ms"]:
            raise HTTPException(400, "Invalid target language")
        
        # Step 1: Save uploaded video
        print("Step 1: Saving video...")
        video_path = file_handler.save_upload(file, prefix="input_video")
        temp_files.append(video_path)
        
        # Step 2: Extract audio
        print("Step 2: Extracting audio...")
        audio_path = file_handler.get_output_path("extracted_audio", ".wav")
        temp_files.append(audio_path)
        video_service.extract_audio(video_path, audio_path)
        
        # Step 3: Transcribe (STT)
        print("Step 3: Transcribing audio...")
        stt = get_stt_service()
        original_text, detected_lang = stt.transcribe(audio_path)
        print(f"Original text: {original_text}")
        
        # Step 4: Translate
        print("Step 4: Translating text...")
        translator = get_translation_service()
        translated_text = translator.translate(
            text=original_text,
            source_lang=source_lang,
            target_lang=target_lang
        )
        print(f"Translated text: {translated_text}")
        
        # Step 5: Text-to-Speech
        print("Step 5: Generating speech...")
        tts = get_tts_service()
        new_audio_path = file_handler.get_output_path("translated_audio", ".mp3")
        temp_files.append(new_audio_path)
        await tts.generate_speech_async(translated_text, target_lang, new_audio_path)
        
        # Step 6: Merge audio with video
        print("Step 6: Creating final video...")
        output_video_path = file_handler.get_output_path("translated_video", ".mp4")
        video_service.replace_audio(video_path, new_audio_path, output_video_path)
        
        print("="*60)
        print("✓ TRANSLATION COMPLETE")
        print("="*60 + "\n")
        
        # Cleanup temp files
        file_handler.cleanup_files(*temp_files)
        
        # Return translated video
        return FileResponse(
            output_video_path,
            media_type="video/mp4",
            filename=f"translated_{Path(video_path).name}"
        )
        
    except Exception as e:
        # Cleanup all temp files on error
        file_handler.cleanup_files(*temp_files)
        print(f"\n✗ Pipeline Error: {e}\n")
        raise HTTPException(status_code=500, detail=str(e))


################ RUN SERVER ################
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )