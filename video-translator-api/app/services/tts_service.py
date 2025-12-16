import edge_tts
import asyncio
import os
from app.models.schemas import SUPPORTED_LANGUAGES

class TTSService:
    """Text-to-Speech using Edge-TTS (Microsoft voices)"""
    
    def __init__(self):
        """Initialize TTS service with voice mapping from registry"""
        # Build voice map from SUPPORTED_LANGUAGES
        self.VOICE_MAP = {
            lang_code: lang_data["tts_voice"]
            for lang_code, lang_data in SUPPORTED_LANGUAGES.items()
        }
        print("✓ Edge-TTS service initialized")
        print(f"✓ Loaded {len(self.VOICE_MAP)} language voices")
    
    async def generate_speech_async(self, text: str, language: str, output_path: str) -> str:
        """
        Async method to generate speech (for use in FastAPI)
        
        Args:
            text: Text to convert
            language: Language code (en, zh-CN, ms)
            output_path: Output audio file path
            
        Returns:
            Path to generated audio file
        """
        try:
            print(f"Generating speech ({language}): {text[:50]}...")
            
            voice = self.VOICE_MAP.get(language, self.VOICE_MAP["en"])
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                if file_size < 1000:
                    raise Exception(f"Audio file too small ({file_size} bytes)")
                
                print(f"✓ Speech generated: {output_path}")
                return output_path
            else:
                raise Exception("Audio file not created")
                
        except Exception as e:
            print(f"✗ TTS Error: {e}")
            raise Exception(f"TTS generation failed: {str(e)}")
    
    def generate_speech(self, text: str, language: str, output_path: str) -> str:
        """
        Convert text to speech
        Sync wrapper for non-async contexts (backward compatibility)

        Args:
            text: Text to convert
            language: Language code (en, zh-CN, ms)
            output_path: Output audio file path
            
        Returns:
            Path to generated audio file
        """
        try:
            # Check if there's already a running event loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # No running loop, safe to use asyncio.run()
                return asyncio.run(self.generate_speech_async(text, language, output_path))
            
                # # If we're here, there's a running loop - shouldn't happen in sync context
                # raise Exception("Cannot use sync method in async context. Use generate_speech_async() instead.")

            print(f"Generating speech ({language}): {text[:50]}...")
            
            # # Run async function
            # asyncio.run(self._generate_speech_async(text, language, output_path))
            
            if os.path.exists(output_path):
                print(f"✓ Speech generated: {output_path}")
                return output_path
            else:
                raise Exception("Audio file not created")
                
        except Exception as e:
            print(f"✗ TTS Error: {e}")
            raise Exception(f"TTS generation failed: {str(e)}")
    
    def get_available_voices(self, language: str = None):
        """Get available voices (for future expansion)"""
        if language:
            return {language: self.VOICE_MAP.get(language, "Unknown")}
        return self.VOICE_MAP