"""
figur.utils
~~~~~~~~~~~

This module implements basic helper functions.
"""

import urllib
from pathlib import Path

import gdown
from spacy.lang.de import German


HOME = Path.home()
CACHE_DIR = Path("models")
CACHE_ROOT = Path(HOME, ".figur")
RESOURCE = {"filename": "figurenerkennung-0.0.1.pt",
            "url": "https://drive.google.com/uc?export=download&confirm=7Eho&id=1UskLtU2aRm6los-zxl4lDRgMRfyV91LX"}


def cached(path: str) -> Path:
    cache = Path(CACHE_ROOT, CACHE_DIR)
    parsed = urllib.parse.urlparse(path)

    if parsed.scheme in {"https"}:
        return _get_from_cache(path, cache)
    elif not parsed.scheme and Path(path).exists():
        return Path(path)
    elif not parsed.scheme and not Path(path).exists():
        raise FileNotFoundError(f"File {path} does not exist.")
    else:
        raise ValueError(f"Unable to parse {path} as URL or as local path.")


def _get_from_cache(url: str, cache: Path) -> Path:
    if not cache.exists():
        cache.mkdir(parents=True)

    filepath = Path(cache, RESOURCE["filename"])

    if filepath.exists():
        return filepath

    gdown.download(url, str(filepath), quiet=False)
    return filepath


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
