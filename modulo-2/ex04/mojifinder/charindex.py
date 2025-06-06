"""
``CharIndex`` creates an inverted index mapping words to sets of Unicode
characters which contain that word in their names.

For example, this indexes the names of Unicode codepoints from 32 to 65::

    >>> index = CharIndex(32, 65)
    >>> sorted(index.index['SIGN'])
    ['#', '$', '%', '+', '<', '=', '>']
    >>> sorted(index.index['DIGIT'])
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

To search for a character named with the words
`'DIGIT'` and `'EIGHT'`::

    >>> index.query(['DIGIT', 'EIGHT'])
    ['8']

"""

import sys
import re
from collections import defaultdict
from unicodedata import name as get_name


RE_WORD = re.compile(r"\w+")
STOP_CODE = sys.maxunicode + 1


InvertedIndex = dict[str, set[str]]


def tokenize(text: str) -> list[str]:
    """split text into a list of uppercased words"""
    return [word.upper() for word in RE_WORD.findall(text)]


class CharIndex:
    def __init__(self, start: int = 32, end: int = STOP_CODE):
        """Initialize the CharIndex with an inverted index."""
        self.index: InvertedIndex = defaultdict(set)
        for char in (chr(i) for i in range(start, end)):
            if name := get_name(char, ""):
                for word in tokenize(name):
                    self.index[word].add(char)
        assert len(self.index) > 0, "No characters indexed."

    def search(self, words: list[str]) -> list[str]:
        """Return list of characters with all words in their names."""
        if not words:
            return []
        first, *rest = words
        try:
            result = self.index[first]
            for word in rest:
                hits = self.index[word]
                result &= hits
                if not result:
                    return []
        except KeyError:
            return []
        return sorted(result)
