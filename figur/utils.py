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
RESOURCE = {"filename": "figurenerkennung-0.0.1.pt",
            "url": "https://drive.google.com/uc?export=download&id=1UskLtU2aRm6los-zxl4lDRgMRfyV91LX"}


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

    response = requests.head(url)
    if response.status_code != 200:
        raise IOError(f"HEAD request failed for URL {url}.")

    _, temp_filepath = tempfile.mkstemp()
    logger.info(f"Downloading from {url} to {temp_filepath}.")
    response = requests.get(url, stream=True)
    content_length = response.headers.get("Content-Length")
    total = int(content_length) if content_length else None
    progress = Tqdm.tqdm(unit="B", total=total)
    with open(temp_filepath, "wb") as temp_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                progress.update(len(chunk))
                temp_file.write(chunk)
    progress.close()

    logger.info(f"Copying {temp_filepath} to cache at {filepath}.")
    shutil.copyfile(temp_filename, str(filepath))
    logger.info(f"Removing temp file {temp_filename}.")
    os.remove(temp_filepath)
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
