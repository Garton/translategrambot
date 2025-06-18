from functools import lru_cache
from typing import List

import spacy

USE_LIGHTWEIGHT_MODEL = True


@lru_cache(1)
def _nlp():
    # lightweight model
    if USE_LIGHTWEIGHT_MODEL:
        lp = spacy.blank("xx")
        lp.add_pipe("sentencizer")
        return lp
    else:  # heavy model, ~2 MB, RAM +40 MB
        return spacy.load("xx_sent_ud_sm")


def split(text: str) -> List[str]:
    """Split text into sentences (UD rules)."""
    return [s.text.strip() for s in _nlp()(text).sents]
