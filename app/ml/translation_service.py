from __future__ import annotations

import logging
import time
from functools import lru_cache
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from app.ml.language_sentence_split import split

logger = logging.getLogger(__name__)

USE_LIGHTWEIGHT_MODEL = True
_MODEL_TPL_LIGHTWEIGHT = "Helsinki-NLP/opus-mt-{src}-{tgt}"
_MODEL_TPL_HEAVY = "facebook/nllb-200-distilled-600M"


DEFAULT_INTERMEDIATE_LANGUAGE = "en"

from app.ml.nllb_codes import NLLB_CODES as _MODEL_TPL_HEAVY_CODE_MAP


class TranslationService:
    """
    Лениво загружает модели opus-mt и кеширует pipeline по паре языков.
    """

    def __init__(self) -> None:
        self._cache: dict[tuple[str, str], pipeline] = {}

    # ---------- PUBLIC ----------
    async def translate(
        self, text: str, src_lang: str, tgt_lang: str, max_new_tokens: int = 128
    ) -> str | None:
        text = text.lstrip("\n\r .,!?")
        text = text.rstrip("\n\r ")

        if not text:
            return None

        pipe = await self._get_pipeline(src_lang, tgt_lang)
        if pipe is None:
            return None

        start = time.perf_counter()
        parts = split(text)

        # optimize for batch processing on cpu
        batch = 8 if len(parts) > 4 else len(parts)

        outs = pipe(
            parts,
            max_new_tokens=max_new_tokens,
            truncation=True,
            batch_size=batch,
        )
        out = " ".join([out["translation_text"] for out in outs])
        logger.info(
            "translate %s→%s %.0f ms len=%d→%d",
            src_lang,
            tgt_lang,
            (time.perf_counter() - start) * 1_000,
            len(text),
            len(out),
        )
        return out

    async def translate_intermediate(
        self, text: str, src_lang: str, tgt_lang: str
    ) -> str | None:
        translated = await self.translate(text, src_lang, tgt_lang)
        if translated:
            return translated
        else:  # trying use intermediate language
            logger.info(
                f"Failed to translate language {src_lang} to {tgt_lang}, trying intermediate language {DEFAULT_INTERMEDIATE_LANGUAGE}"
            )
            translated_intermediate = await self.translate(
                text, src_lang, DEFAULT_INTERMEDIATE_LANGUAGE
            )
            if translated_intermediate:
                translated = await self.translate(
                    translated_intermediate, DEFAULT_INTERMEDIATE_LANGUAGE, tgt_lang
                )
                if translated:
                    return translated
            else:
                logger.info(
                    f"Failed to translate language {src_lang} through intermediate language {DEFAULT_INTERMEDIATE_LANGUAGE} to {tgt_lang}"
                )
        return None

    # ---------- PRIVATE ----------
    async def _get_pipeline(self, src_lang: str, tgt_lang: str) -> pipeline | None:
        key = (src_lang, tgt_lang)
        if key in self._cache:
            return self._cache[key]

        model_name, src_lang, tgt_lang = self._select_model(src_lang, tgt_lang)

        try:
            logger.info("loading model %s …", model_name)
            tok = AutoTokenizer.from_pretrained(model_name)
            mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            pipe = pipeline(
                "translation",
                model=mdl,
                tokenizer=tok,
                src_lang=src_lang,
                tgt_lang=tgt_lang,
            )
        except Exception as e:
            logger.warning("model %s unavailable: %s", model_name, e)
            return None

        self._cache[key] = pipe
        return pipe

    def _select_model(self, src_lang: str, tgt_lang: str) -> str:
        if USE_LIGHTWEIGHT_MODEL:
            model = _MODEL_TPL_LIGHTWEIGHT.format(src=src_lang, tgt=tgt_lang)
            return (model, src_lang, tgt_lang)
        else:
            model = _MODEL_TPL_HEAVY
            src_lang = _MODEL_TPL_HEAVY_CODE_MAP.get(src_lang, src_lang)
            tgt_lang = _MODEL_TPL_HEAVY_CODE_MAP.get(tgt_lang, tgt_lang)
            return (model, src_lang, tgt_lang)
