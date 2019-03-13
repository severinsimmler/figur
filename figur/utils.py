"""
figur.utils
~~~~~~~~~~~

This module implements basic helper functions.
"""

import urllib
from pathlib import Path

from spacy.lang.de import German

from . import zenodo


HOME = Path.home()
CACHE_DIR = Path("models")
CACHE_ROOT = Path(HOME, ".figur")
RESOURCE = {"filename": "figurenerkennung-0.0.1.pt",
            "doi": "10.5281/zenodo.2592325"}


def cached(path: str) -> Path:
    cache = Path(CACHE_ROOT, CACHE_DIR, path)
    if cache.exists():
        return cache
    else:
        return _get_from_cache(RESOURCE["doi"], cache)


def _get_from_cache(doi: str, cache: Path) -> Path:
    if not cache.parent.exists():
        cache.parent.mkdir(parents=True)
    return zenodo.download(doi, str(cache))


def segment(text: str):
    nlp = German()
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    document = nlp(text)
    for sentence in document.sents:
        yield sentence.text


def process(text: str, model):
    tagged = {"SentenceId": list(),
              "Token": list(),
              "Tag": list()}
    for n, sentence in enumerate(segment(text)):
        prediction = model.predict(sentence)
        for word, tag in prediction:
            tagged["SentenceId"].append(n)
            tagged["Token"].append(word)
            tagged["Tag"].append(tag.title() if tag == "pron" else tag)
    return tagged
