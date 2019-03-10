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
PRONOUNS = set(["alle", "allen", "aller", "beide", "beiden", "beyde", "dasjenige",
                "dasselbe", "dein", "deine", "deinem", "deinen", "deiner", "deines",
                "denen", "denselben", "deren", "derer", "derjenige", "derselbe",
                "derselben", "desselben", "desselbigen", "dessen", "dich", "diejenige",
                "diejenigen", "diese", "dieselbe", "dieselben", "diesem", "diesen",
                "dieser", "dir", "du", "einander", "er", "erstere", "ersterer",
                "es", "euch", "euer", "eurer", "ich", "ick", "ihm", "ihme", "ihn",
                "ihne", "ihnen", "ihns", "ihr", "ihre", "ihrem", "ihren", "ihrer",
                "ihrerseits", "ihres", "ihretwillen", "ihrige", "ihrigen", "jedem",
                "jeden", "jeder", "jedes", "jemand", "jene", "jenem", "jener",
                "keiner", "letzte", "letztere", "letzterer", "man", "manche",
                "manchem", "mancher", "me", "mei", "mein", "meine", "meinem",
                "meinen", "meiner", "meines", "meinet", "meinigen", "mich", "mir",
                "niemand", "seim", "sein", "seine", "seinem", "seinen", "seiner",
                "seinerseits", "seines", "seinetwegen", "seinetwillen", "seinige",
                "seinigen", "selber", "selbiger", "sich", "sichs", "sie", "uns",
                "unser", "unsere", "unserem", "unseren", "unserer", "unseres",
                "unseresgleichen", "unserm", "unsern", "unsers", "unsre", "unsrem",
                "unsren", "unsrer", "unsrige", "verschiedene", "viele", "vous",
                "welche", "welchem", "welchen", "welcher", "welches", "wir", "état",
                "übrigen"])


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
            tagged["Tag"].append(tag)
    return tagged
