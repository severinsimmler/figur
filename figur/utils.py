import os
import logging
import re
import shutil
import tempfile
import urllib
from pathlib import Path
from tqdm import tqdm as _tqdm

import requests
from spacy.lang.de import German


HOME = Path.home()
CACHE_DIR = Path("models")
CACHE_ROOT = Path(HOME, ".figur")
URL = "https://drive.google.com/figurenerkennung-0.0.1.pt"


def cached(path: str) -> Path:
    """Download model and/or get filepath from cache.
    """
    cache = Path(CACHE_ROOT, CACHE_DIR)
    parsed = urllib.parse.urlparse(path)
    path = Path(path)

    if parsed.scheme in {"https"}:
        return _get_from_cache(path, cache)
    elif not parsed.scheme and path.exists():
        return Path(path)
    elif not parsed.scheme and not path.exists():
        raise FileNotFoundError(f"File {path} does not exist.")
    else:
        raise ValueError(f"Unable to parse {path} as URL or as local path.")


def _get_from_cache(url: Path, cache: Path) -> Path:
    if not cache.exists():
        cache.mkdir(parents=True)
    filepath = Path(cache, url.name)

    if filepath.exists():
        return filepath

    response = requests.head(url)
    if response.status_code != 200:
        raise IOError(f"HEAD request failed for URL {url}.")

    if not filepath.exists():
        _, temp_filepath = tempfile.mkstemp()
        logger.info(f"Downloading from {url} to {temp_filepath}.")
        response = requests.get((url), stream=True)
        content_length = response.headers.get("Content-Length")
        total = int(content_length) if content_length else None
        progress = Tqdm.tqdm(unit="B", total=total)
        with open(temp_filename, "wb") as temp_file:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    progress.update(len(chunk))
                    temp_file.write(chunk)
        progress.close()

        logger.info(f"Copying {temp_filename} to cache at {filepath}.")
        shutil.copyfile(temp_filename, str(filepath))
        logger.info(f"Removing temp file {temp_filename}.")
        os.remove(temp_filename)
    return filepath


class Tqdm:
    default_mininterval: float = 0.1

    @staticmethod
    def set_default_mininterval(value: float) -> None:
        Tqdm.default_mininterval = value

    @staticmethod
    def set_slower_interval(use_slower_interval: bool) -> None:
        if use_slower_interval:
            Tqdm.default_mininterval = 10.0
        else:
            Tqdm.default_mininterval = 0.1

    @staticmethod
    def tqdm(*args, **kwargs):
        new_kwargs = {"mininterval": Tqdm.default_mininterval,
                      **kwargs}
        return _tqdm(*args, **new_kwargs)


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
