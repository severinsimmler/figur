import pytest
import figur


TEXT = "Der Gärtner entfernte sich eilig, und Eduard folgte bald."

def test_tagging():
    tagged = figur.tag(TEXT)
    counts = tagged["Tag"].value_counts()
    assert counts["AppTdfW"] == 1
    assert counts["pron"] == 1
    assert counts["Core"] == 1
    assert counts["_"] == 6
