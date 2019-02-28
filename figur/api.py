"""
figur.api
~~~~~~~~~

This module implements the high-level API.
"""

import pandas as pd

from . import model
from . import utils


URL = utils.RESOURCE["url"]
PATH = utils.cached(URL)
TAGGER = model.Model(PATH)


def tag(text: str) -> pd.DataFrame:
    """Tag named entities in a given text.
    """
    tagged = utils.process(text, TAGGER)
    return pd.DataFrame(tagged)
