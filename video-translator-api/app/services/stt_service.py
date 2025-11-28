import whisper
import os
from typing import Tuple

class STTService:
    """Speech-to-Text using OpenAI Whisper"""
    
    def __init__(self, model_size: str = "tiny"):
        """
        Initialize Whisper model
        Models: tiny, base, small, medium, large
        base = good balance (74MB, ~5x faster than large)
        """
        print(f"Loading Whisper model: {model_size}...")
        self.model = whisper.load_model(model_size)
        print("✓ Whisper model loaded")
    
    def transcribe(self, audio_path: str) -> Tuple[str, str]:
        """
        Transcribe audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Tuple of (transcribed_text, detected_language)
        """
        try:
            print(f"Transcribing: {audio_path}")
            
            # Whisper auto-detects language
            result = self.model.transcribe(
                audio_path,
                fp16=False,  # Use FP32 for CPU (Windows compatibility)
                language=None  # Auto-detect
            )
            
            text = result["text"].strip()
            detected_lang = result["language"]
            
            print(f"✓ Transcribed ({detected_lang}): {text[:100]}...")
            
            return text, detected_lang
            
        except Exception as e:
            print(f"✗ STT Error: {e}")
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_with_language(self, audio_path: str, language: str) -> str:
        """
        Transcribe with specified language (faster)
        
        Args:
            audio_path: Path to audio file
            language: Language code (en, zh, ms)
            
        Returns:
            Transcribed text
        """
        try:
            result = self.model.transcribe(
                audio_path,
                fp16=False,
                language=language
            )
            
            return result["text"].strip()
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")