"""
figur.model
~~~~~~~~~~~

This module implements the NER model class.
"""

from pathlib import Path

from flair.models import SequenceTagger
from flair.data import Sentence


class Model:
    def __init__(self, path: Path):
        self.path = path
        self.tagger = SequenceTagger.load_from_file(path)

    def predict(self, sentence: str):
        """Predict labels for a given sentence.
        """
        s = Sentence(sentence)
        self.tagger.predict(s)
        for word in s:
            yield s["token"], s["tag"]
