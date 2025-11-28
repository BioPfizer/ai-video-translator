from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class LanguageCode(str, Enum):
    """Supported language codes"""
    ENGLISH = "en"
    CHINESE = "zh-CN"
    MALAY = "ms"

class TranslationRequest(BaseModel):
    text: str = Field(..., description="Text to translate")
    source_lang: LanguageCode = Field(..., description="Source language")
    target_lang: LanguageCode = Field(..., description="Target language")

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    language: LanguageCode = Field(..., description="Language of the text")

class STTResponse(BaseModel):
    text: str
    language: str
    duration: float

class VideoTranslationRequest(BaseModel):
    source_lang: LanguageCode
    target_lang: LanguageCode

class VideoTranslationResponse(BaseModel):
    job_id: str
    status: str
    original_text: Optional[str] = None
    translated_text: Optional[str] = None
    output_file: Optional[str] = None