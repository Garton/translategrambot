import logging
import time
from typing import Optional

from langdetect import DetectorFactory, LangDetectException, detect_langs
from lingua import Language, LanguageDetectorBuilder

logger = logging.getLogger(__name__)

_MIN_LEN = 10  # less than 10 chars — noise
_MAIN_THRESHOLD = 0.90  # langdetect: minimum confidence


class LanguageService:
    def __init__(self) -> None:
        DetectorFactory.seed = 0
        # --- initialize once ---
        self._lingua = (
            LanguageDetectorBuilder.from_all_languages()
            .with_low_accuracy_mode()
            .build()
        )

    # ---------- PUBLIC --------------------------------------------------
    def detect(self, text: str) -> Optional[str]:
        """Return ISO code of language or None."""
        if not self._is_valid(text):
            return None

        iso = self._primary_detector(text)
        if iso:
            return iso

        return self._fallback_detector(text)

    # ---------- PRIVATE -------------------------------------------------
    @staticmethod
    def _is_valid(text: str) -> bool:
        return bool(text and not text.isspace() and not text.isnumeric())

    def _primary_detector(self, text: str) -> Optional[str]:
        """langdetect with length and confidence filters."""
        if len(text) < _MIN_LEN:
            return None
        try:
            top = detect_langs(text)[0]  # lang:prob
        except LangDetectException:
            return None

        if top.prob >= _MAIN_THRESHOLD:
            logger.debug("primary ok: %s %.2f", top.lang, top.prob)
            return top.lang
        logger.debug("primary low-conf: %s %.2f", top.lang, top.prob)
        return None

    def _fallback_detector(self, text: str) -> str | None:
        language = self._lingua.detect_language_of(text)
        if not language:
            return None

        confidence = self._lingua.compute_language_confidence(text, language)
        logger.debug(
            "lingua iso=%s conf=%.2f", language.iso_code_639_1.name, confidence
        )

        if confidence >= 0.90:  # threshold
            return language.iso_code_639_1.name.lower()
        return None
