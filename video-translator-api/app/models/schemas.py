from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class LanguageCode(str, Enum):
    """Supported language codes"""
    # Western Languages
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    PORTUGUESE = "pt"
    ITALIAN = "it"
    DUTCH = "nl"
    RUSSIAN = "ru"
    POLISH = "pl"
    SWEDISH = "sv"
    NORWEGIAN = "no"
    DANISH = "da"
    FINNISH = "fi"
    ESTONIAN = "et"
    LATVIAN = "lv"
    LITHUANIAN = "lt"
    CZECH = "cs"
    SLOVAK = "sk"
    HUNGARIAN = "hu"
    BULGARIAN = "bg"
    ROMANIAN = "ro"
    CATALAN = "ca"
    GREEK = "el"
    UKRAINIAN = "uk"
    
    # East Asian Languages
    CHINESE_SIMPLIFIED = "zh-CN"
    # CHINESE_TRADITIONAL = "zh-TW"
    JAPANESE = "ja"
    KOREAN = "ko"

    # Southeast Asian Languages
    MALAY = "ms"
    INDONESIAN = "id"
    THAI = "th"
    VIETNAMESE = "vi"
    
    # South Asian Languages
    HINDI = "hi"
    TAMIL = "ta"
    URDU = "ur"
    
    # Middle Eastern Languages
    ARABIC = "ar"
    TURKISH = "tr"

# Complete language metadata registry
SUPPORTED_LANGUAGES = {
    # === Western European Languages ===
    "en": {
        "name": "English",
        "native_name": "English",
        "flag": "🇬🇧",
        "tts_voice": "en-US-AriaNeural",
        "stt_supported": True,
        "deepgram_code": "en",
        "deepgram_model": "nova-3"
    },
    "es": {
        "name": "Spanish",
        "native_name": "Español",
        "flag": "🇪🇸",
        "tts_voice": "es-ES-ElviraNeural",
        "stt_supported": True,
        "deepgram_code": "es",
        "deepgram_model": "nova-3"
    },
    "fr": {
        "name": "French",
        "native_name": "Français",
        "flag": "🇫🇷",
        "tts_voice": "fr-FR-DeniseNeural",
        "stt_supported": True,
        "deepgram_code": "fr",
        "deepgram_model": "nova-3"
    },
    "de": {
        "name": "German",
        "native_name": "Deutsch",
        "flag": "🇩🇪",
        "tts_voice": "de-DE-KatjaNeural",
        "stt_supported": True,
        "deepgram_code": "de",
        "deepgram_model": "nova-3"
    },
    "pt": {
        "name": "Portuguese",
        "native_name": "Português",
        "flag": "🇵🇹",
        "tts_voice": "pt-PT-RaquelNeural",
        "stt_supported": True,
        "deepgram_code": "pt",
        "deepgram_model": "nova-3"
    },
    "it": {
        "name": "Italian",
        "native_name": "Italiano",
        "flag": "🇮🇹",
        "tts_voice": "it-IT-ElsaNeural",
        "stt_supported": True,
        "deepgram_code": "it",
        "deepgram_model": "nova-3"
    },
    "nl": {
        "name": "Dutch",
        "native_name": "Nederlands",
        "flag": "🇳🇱",
        "tts_voice": "nl-NL-ColetteNeural",
        "stt_supported": True,
        "deepgram_code": "nl",
        "deepgram_model": "nova-3"
    },
    "ru": {
        "name": "Russian",
        "native_name": "Русский",
        "flag": "🇷🇺",
        "tts_voice": "ru-RU-SvetlanaNeural",
        "stt_supported": True,
        "deepgram_code": "ru",
        "deepgram_model": "nova-3"
    },
    "pl": {
        "name": "Polish",
        "native_name": "Polski",
        "flag": "🇵🇱",
        "tts_voice": "pl-PL-ZofiaNeural",
        "stt_supported": True,
        "deepgram_code": "pl",
        "deepgram_model": "nova-3"
    },
    "sv": {
        "name": "Swedish",
        "native_name": "Svenska",
        "flag": "🇸🇪",
        "tts_voice": "sv-SE-SofieNeural",
        "stt_supported": True,
        "deepgram_code": "sv",
        "deepgram_model": "nova-3"
    },
    "no": {
        "name": "Norwegian",
        "native_name": "Norsk",
        "flag": "🇳🇴",
        "tts_voice": "nb-NO-PernilleNeural",
        "stt_supported": True,
        "deepgram_code": "no",
        "deepgram_model": "nova-3"
    },
    "da": {
        "name": "Danish",
        "native_name": "Dansk",
        "flag": "🇩🇰",
        "tts_voice": "da-DK-ChristelNeural",
        "stt_supported": True,
        "deepgram_code": "da",
        "deepgram_model": "nova-3"
    },
    "fi": {
        "name": "Finnish",
        "native_name": "Suomi",
        "flag": "🇫🇮",
        "tts_voice": "fi-FI-NooraNeural",
        "stt_supported": True,
        "deepgram_code": "fi",
        "deepgram_model": "nova-3"
    },
    
    # === Eastern European ===
    "et": {
        "name": "Estonian",
        "native_name": "Eesti",
        "flag": "🇪🇪",
        "tts_voice": "et-EE-AnuNeural",
        "stt_supported": True,
        "deepgram_code": "et",
        "deepgram_model": "nova-3"
    },
    "lv": {
        "name": "Latvian",
        "native_name": "Latviešu",
        "flag": "🇱🇻",
        "tts_voice": "lv-LV-EveritaNeural",
        "stt_supported": True,
        "deepgram_code": "lv",
        "deepgram_model": "nova-3"
    },
    "lt": {
        "name": "Lithuanian",
        "native_name": "Lietuvių",
        "flag": "🇱🇹",
        "tts_voice": "lt-LT-OnaNeural",
        "stt_supported": True,
        "deepgram_code": "lt",
        "deepgram_model": "nova-3"
    },
    "cs": {
        "name": "Czech",
        "native_name": "Čeština",
        "flag": "🇨🇿",
        "tts_voice": "cs-CZ-VlastaNeural",
        "stt_supported": True,
        "deepgram_code": "cs",
        "deepgram_model": "nova-3"
    },
    "sk": {
        "name": "Slovak",
        "native_name": "Slovenčina",
        "flag": "🇸🇰",
        "tts_voice": "sk-SK-ViktoriaNeural",
        "stt_supported": True,
        "deepgram_code": "sk",
        "deepgram_model": "nova-3"
    },
    "hu": {
        "name": "Hungarian",
        "native_name": "Magyar",
        "flag": "🇭🇺",
        "tts_voice": "hu-HU-NoemiNeural",
        "stt_supported": True,
        "deepgram_code": "hu",
        "deepgram_model": "nova-3"
    },
    "bg": {
        "name": "Bulgarian",
        "native_name": "Български",
        "flag": "🇧🇬",
        "tts_voice": "bg-BG-KalinaNeural",
        "stt_supported": True,
        "deepgram_code": "bg",
        "deepgram_model": "nova-3"
    },
    "ro": {
        "name": "Romanian",
        "native_name": "Română",
        "flag": "🇷🇴",
        "tts_voice": "ro-RO-AlinaNeural",
        "stt_supported": True,
        "deepgram_code": "ro",
        "deepgram_model": "nova-3"
    },
    "ca": {
        "name": "Catalan",
        "native_name": "Català",
        "flag": "🇪🇸",
        "tts_voice": "ca-ES-JoanaNeural",
        "stt_supported": True,
        "deepgram_code": "ca",
        "deepgram_model": "nova-3"
    },
    "el": {
        "name": "Greek",
        "native_name": "Ελληνικά",
        "flag": "🇬🇷",
        "tts_voice": "el-GR-AthinaNeural",
        "stt_supported": True,
        "deepgram_code": "el",
        "deepgram_model": "nova-3"
    },
    "uk": {
        "name": "Ukrainian",
        "native_name": "Українська",
        "flag": "🇺🇦",
        "tts_voice": "uk-UA-PolinaNeural",
        "stt_supported": True,
        "deepgram_code": "uk",
        "deepgram_model": "nova-3"
    },
    
    # === East Asian Languages ===
    "zh-CN": {
        "name": "Chinese (Simplified)",
        "native_name": "简体中文",
        "flag": "🇨🇳",
        "tts_voice": "zh-CN-XiaoxiaoNeural",
        "stt_supported": True,
        "deepgram_code": "zh",
        "deepgram_model": "nova-2"  # Note: Chinese only in Nova-2
    },
    "zh-TW": {
        "name": "Chinese (Traditional)",
        "native_name": "繁體中文",
        "flag": "🇹🇼",
        "tts_voice": "zh-TW-HsiaoChenNeural",
        "stt_supported": True,
        "deepgram_code": "zh-TW",
        "deepgram_model": "nova-2"  # Note: Chinese only in Nova-2
    },
    "ja": {
        "name": "Japanese",
        "native_name": "日本語",
        "flag": "🇯🇵",
        "tts_voice": "ja-JP-NanamiNeural",
        "stt_supported": True,
        "deepgram_code": "ja",
        "deepgram_model": "nova-3"
    },
    "ko": {
        "name": "Korean",
        "native_name": "한국어",
        "flag": "🇰🇷",
        "tts_voice": "ko-KR-SunHiNeural",
        "stt_supported": True,
        "deepgram_code": "ko",
        "deepgram_model": "nova-3"
    },
    
    # === Southeast Asian Languages ===
    "ms": {
        "name": "Malay",
        "native_name": "Bahasa Melayu",
        "flag": "🇲🇾",
        "tts_voice": "ms-MY-OsmanNeural",
        "stt_supported": True,
        "deepgram_code": "ms",
        "deepgram_model": "nova-3"
    },
    "id": {
        "name": "Indonesian",
        "native_name": "Bahasa Indonesia",
        "flag": "🇮🇩",
        "tts_voice": "id-ID-ArdiNeural",
        "stt_supported": True,
        "deepgram_code": "id",
        "deepgram_model": "nova-3"
    },
    "th": {
        "name": "Thai",
        "native_name": "ไทย",
        "flag": "🇹🇭",
        "tts_voice": "th-TH-PremwadeeNeural",
        "stt_supported": True,
        "deepgram_code": "th",
        "deepgram_model": "nova-2"  # Note: Thai only in Nova-2
    },
    "vi": {
        "name": "Vietnamese",
        "native_name": "Tiếng Việt",
        "flag": "🇻🇳",
        "tts_voice": "vi-VN-HoaiMyNeural",
        "stt_supported": True,
        "deepgram_code": "vi",
        "deepgram_model": "nova-3"
    },
    
    # === South Asian Languages ===
    "hi": {
        "name": "Hindi",
        "native_name": "हिन्दी",
        "flag": "🇮🇳",
        "tts_voice": "hi-IN-SwaraNeural",
        "stt_supported": True,
        "deepgram_code": "hi",
        "deepgram_model": "nova-3"
    },
    "ta": {
        "name": "Tamil",
        "native_name": "தமிழ்",
        "flag": "🇮🇳",
        "tts_voice": "ta-IN-PallaviNeural",
        "stt_supported": False,  # NOT in Deepgram docs
        "deepgram_code": None,
        "deepgram_model": None
    },
    "ur": {
        "name": "Urdu",
        "native_name": "اردو",
        "flag": "🇵🇰",
        "tts_voice": "ur-PK-UzmaNeural",
        "stt_supported": False,  # NOT in Deepgram docs
        "deepgram_code": None,
        "deepgram_model": None
    },
    
    # === Middle Eastern Languages ===
    "ar": {
        "name": "Arabic",
        "native_name": "العربية",
        "flag": "🇸🇦",
        "tts_voice": "ar-SA-ZariyahNeural",
        "stt_supported": False,  # NOT in Deepgram Nova-3 docs
        "deepgram_code": None,
        "deepgram_model": None
    },
    "tr": {
        "name": "Turkish",
        "native_name": "Türkçe",
        "flag": "🇹🇷",
        "tts_voice": "tr-TR-EmelNeural",
        "stt_supported": True,
        "deepgram_code": "tr",
        "deepgram_model": "nova-3"
    },
}

# Helper function to get language info
def get_language_info(lang_code: str) -> dict:
    """Get language information by code"""
    return SUPPORTED_LANGUAGES.get(lang_code, SUPPORTED_LANGUAGES["en"])

# Helper function to validate language
def is_language_supported(lang_code: str) -> bool:
    """Check if language is supported"""
    return lang_code in SUPPORTED_LANGUAGES

def get_stt_supported_languages() -> dict:
    """Get only languages with STT support"""
    return {
        code: info for code, info in SUPPORTED_LANGUAGES.items()
        if info.get("stt_supported", False)
    }

def get_translation_only_languages() -> dict:
    """Get languages that only support translation (no STT)"""
    return {
        code: info for code, info in SUPPORTED_LANGUAGES.items()
        if not info.get("stt_supported", False)
    }

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