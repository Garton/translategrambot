"""
Facade service: single instances available via short imports
app.services.language_service  /  app.services.translation_service
"""

from app.ml.language_service import LanguageService
from app.ml.translation_service import TranslationService

language_service = LanguageService()
translation_service = TranslationService()

__all__ = [
    "language_service",
    "translation_service",
]
