from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import os
from typing import Tuple

class STTService:
    """Speech-to-Text using Deepgram API"""
    
    def __init__(self):
        """
        Initialize Deepgram client
        Requires DEEPGRAM_API_KEY environment variable
        """
        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        
        if not self.api_key:
            raise ValueError("DEEPGRAM_API_KEY environment variable not set")
        
        self.client = DeepgramClient(self.api_key)
        print("✓ Deepgram STT service initialized")

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
            
            # Read audio file
            with open(audio_path, "rb") as audio_file:
                buffer_data = audio_file.read()
            
            # Prepare audio payload
            payload: FileSource = {
                "buffer": buffer_data,
            }
            
            # Configure Deepgram options
            options = PrerecordedOptions(
                model="nova-2",  # Best general model
                smart_format=True,  # Auto punctuation and formatting
                language="multi",  # Auto-detect language
                detect_language=True,  # Return detected language
            )
            
            # Transcribe
            response = self.client.listen.prerecorded.v("1").transcribe_file(
                payload, options
            )
            
            # Extract text and language
            transcript = response.results.channels[0].alternatives[0].transcript
            detected_lang = response.results.channels[0].detected_language
            
            # Map Deepgram language codes to our format
            lang_map = {
                "en": "en",
                "zh": "zh-CN",
                "zh-CN": "zh-CN",
                "zh-TW": "zh-CN",
                "ms": "ms",
                "id": "ms",  # Indonesian (similar to Malay)
            }
            
            mapped_lang = lang_map.get(detected_lang, "en")
            
            print(f"✓ Transcribed ({detected_lang} → {mapped_lang}): {transcript[:100]}...")
            
            return transcript.strip(), mapped_lang
            
        except Exception as e:
            print(f"✗ Deepgram STT Error: {e}")
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_with_language(self, audio_path: str, language: str) -> str:
        """
        Transcribe with specified language (faster, more accurate)
        
        Args:
            audio_path: Path to audio file
            language: Language code (en, zh-CN, ms)
            
        Returns:
            Transcribed text
        """
        try:
            print(f"Transcribing with language hint: {language}")
            
            # Read audio file
            with open(audio_path, "rb") as audio_file:
                buffer_data = audio_file.read()
            
            payload: FileSource = {
                "buffer": buffer_data,
            }
            
            # Map our language codes to Deepgram's
            lang_map = {
                "en": "en",
                "zh-CN": "zh",
                "ms": "ms",
            }
            
            deepgram_lang = lang_map.get(language, "en")
            
            # Configure options with specific language
            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                language=deepgram_lang,
            )
            
            # Transcribe
            response = self.client.listen.prerecorded.v("1").transcribe_file(
                payload, options
            )
            
            transcript = response.results.channels[0].alternatives[0].transcript
            
            print(f"✓ Transcribed: {transcript[:100]}...")
            
            return transcript.strip()
            
        except Exception as e:
            print(f"✗ Deepgram STT Error: {e}")
            raise Exception(f"Transcription failed: {str(e)}")