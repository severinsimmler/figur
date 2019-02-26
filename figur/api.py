"""
figur.api
~~~~~~~~~

This module implements the high-level API.
"""

import pandas as pd

from . import model
from . import utils


def tag(text: str) -> pd.DataFrame:
    """Tag named entities in the text.
    """
    path = utils.cached(utils.URL)
    tagger = model.Model(path)
    tagged = utils.process(text, tagger)
    return pd.DataFrame(tagged)
