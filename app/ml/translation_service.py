from __future__ import annotations

import logging
import time
from functools import lru_cache
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

logger = logging.getLogger(__name__)

_MODEL_TPL = "Helsinki-NLP/opus-mt-{src}-{tgt}"
_MAX_TOKENS = 512


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
        if not text.strip():
            return None
        pipe = await self._get_pipeline(src_lang, tgt_lang)
        if pipe is None:
            return None

        start = time.perf_counter()
        out = pipe(
            text,
            max_length=_MAX_TOKENS,
            max_new_tokens=max_new_tokens,
            truncation=True,
        )[0]["translation_text"]
        logger.info(
            "translate %s→%s %.0f ms len=%d→%d",
            src_lang,
            tgt_lang,
            (time.perf_counter() - start) * 1_000,
            len(text),
            len(out),
        )
        return out

    # ---------- PRIVATE ----------
    async def _get_pipeline(self, src_lang: str, tgt_lang: str) -> pipeline | None:
        key = (src_lang, tgt_lang)
        if key in self._cache:
            return self._cache[key]

        model_name = _MODEL_TPL.format(src=src_lang, tgt=tgt_lang)
        try:
            logger.info("loading model %s …", model_name)
            tok = AutoTokenizer.from_pretrained(model_name)
            mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            pipe = pipeline("translation", model=mdl, tokenizer=tok)
        except Exception as e:
            logger.warning("model %s unavailable: %s", model_name, e)
            return None

        self._cache[key] = pipe
        return pipe
