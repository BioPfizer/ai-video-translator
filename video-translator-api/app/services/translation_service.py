from deep_translator import GoogleTranslator, DeeplTranslator
from typing import Dict

# Google Translator
class TranslationService:
    """Translation service using Google Translate (free)"""
    
    # Language code mapping
    LANG_MAP = {
        "en": "en",
        "zh-CN": "zh-CN",
        "ms": "ms",
        "zh": "zh-CN"  # Alias
    }
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        try:
            # Normalize language codes
            source = self.LANG_MAP.get(source_lang, source_lang)
            target = self.LANG_MAP.get(target_lang, target_lang)
            
            # Skip if same language
            if source == target:
                return text
            
            print(f"Translating: {source} → {target}")
            print(f"Original: {text[:100]}...")
            
            # Translate
            translator = GoogleTranslator(source=source, target=target)
            translated = translator.translate(text)
            
            print(f"Translated: {translated[:100]}...")
            
            return translated
            
        except Exception as e:
            print(f"✗ Translation Error: {e}")
            raise Exception(f"Translation failed: {str(e)}")
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            from deep_translator import single_detection
            lang = single_detection(text, api_key=None)
            return self.LANG_MAP.get(lang, lang)
        except:
            return "en"  # Default to English

# DeepL Translator
class TranslationService2:
    def __init__(self, use_deepl: bool = False, deepl_api_key: str = None):
        self.use_deepl = use_deepl
        self.deepl_api_key = deepl_api_key
    
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if self.use_deepl and self.deepl_api_key:
            # Use DeepL (better quality)
            translator = DeeplTranslator(
                api_key=self.deepl_api_key,
                source=source_lang,
                target=target_lang
            )
        else:
            # Use Google (free)
            translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        return translator.translate(text)