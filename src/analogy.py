from collections import defaultdict
from collections.abc import Callable

from src.analysis import Word, WordDict

type Analogies = dict[tuple[str, str], float]


def find_analogies(
    word_dict: WordDict, bigram: tuple[str, str], all_bigrams: set[tuple[str, str]]
) -> Analogies:
    """
    Finds the analogies of bigram in the training data and calculates by how much they increase the probality of the bigram.
    """

    analogies: Analogies = {}
    get_word = word_dict.__getitem__  # avoiding global lookups per call

    b1, b2 = bigram

    w1 = get_word(b1)
    w2 = get_word(b2)

    w1_befores = w1.before
    w1_afters = w1.after
    w1_freq = w1.freq

    w2_befores = w2.before
    w2_afters = w2.after
    w2_freq = w2.freq

    for anal1 in word_dict:
        a1 = get_word(anal1)
        a1_after_keys = a1.after.keys()
        a1_before_keys = a1.before.keys()

        for anal2 in a1_after_keys:
            a2 = get_word(anal2)
            common_of_1_before = set(w1_befores.keys()).intersection(
                set(a1_before_keys)
            )
            common_of_1_after = set(w1_afters.keys()).intersection(set(a1_after_keys))

            common_of_2_before = set(w2_befores.keys()).intersection(
                set(a2.before.keys())
            )
            common_of_2_after = set(w2_afters.keys()).intersection(set(a2.after.keys()))

            s1 = calc_similarity(
                w1_freq,
                w1_befores,
                w1_afters,
                anal1,
                common_of_1_before,
                common_of_1_after,
                get_word,
            )
            s2 = calc_similarity(
                w2_freq,
                w2_befores,
                w2_afters,
                anal2,
                common_of_2_before,
                common_of_2_after,
                get_word,
            )

            s = min(s1, s2)

            if s != 0:
                analogies[(anal1, anal2)] = s

    return analogies


def calc_similarity(
    word_freq: float,
    word_befores: defaultdict[str, int],
    word_afters: defaultdict[str, int],
    anal: str,
    common_before: set[str],
    common_after: set[str],
    get_word: Callable[[str], Word],
) -> float:
    sl: float = 0
    sr: float = 0

    for x in common_before:
        wx = get_word(x)
        sl += min(word_befores[x] / word_freq, wx.after[anal] / wx.freq)

    for y in common_after:
        wy = get_word(y)
        sr += min(word_afters[y] / word_freq, wy.before[anal] / wy.freq)

    return min(sl, sr)
