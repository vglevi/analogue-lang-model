from collections import defaultdict
from src.corpus import Sentences

class Word:
    '''
    Attributes:
    - freq: frequency of the word
    - before: a dictionary containing which and how frequent words appear before the word
    - after: a dictionary containing which and how frequent words appear after the word
    '''
    def __init__(self) -> None:
        self.freq = 0
        self.before: defaultdict[str, int] = defaultdict(int)
        self.after: defaultdict[str, int] = defaultdict(int)

    def __repr__(self) -> str:
        return f"\nFreq = {self.freq}\nBefore: {self.before.items()}\nAfter: {self.after.items()}\n"

type WordDict = defaultdict[str, Word]

def analyze_corpus(corpus: Sentences) -> WordDict:
    '''
    Returns a dictionary whose keys are words and whose values are :class:`Word` objects.
    The corpus argument should be a list of sentences (a sentence is a list of words).
    '''
    word_dict: WordDict = defaultdict(Word)
    for sentence in corpus:
        if len(sentence) == 0:
            continue

        first = word_dict[sentence[0]]
        first.freq += 1
        if len(sentence) > 1:
            first.after[sentence[1]] += 1

            last = word_dict[sentence[-1]]
            last.freq += 1
            last.before[sentence[-2]] += 1

        for wi in range(1, len(sentence) - 1):
            curr = word_dict[sentence[wi]]
            curr.freq += 1
            curr.before[sentence[wi - 1]] += 1
            curr.after[sentence[wi + 1]] += 1

    return word_dict
