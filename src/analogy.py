from collections import defaultdict
from collections.abc import Callable

from src.analysis import Word, WordDict

type Analogies = dict[tuple[str, str], float]


def find_analogies(word_dict: WordDict, bigram: tuple[str, str]) -> Analogies:
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

    a1_sl_d: defaultdict[str, float] = defaultdict(float)
    for x1 in w1_befores:
        wx1 = get_word(x1)
        wx1_afters = wx1.after
        for a1 in wx1_afters:
            a1_sl_d[a1] += min(w1_befores[x1] / w1_freq, wx1_afters[a1] / wx1.freq)

    a1_sr_d: defaultdict[str, float] = defaultdict(float)
    for y1 in w1_afters:
        wy1 = get_word(y1)
        wy1_befores = wy1.before
        for a1 in wy1_befores:
            a1_sr_d[a1] += min(w1_afters[y1] / w1_freq, wy1_befores[a1] / wy1.freq)

    possible_a1s: dict[str, float] = {}
    for a1, sl in a1_sl_d.items():
        s = min(sl, a1_sr_d[a1])
        if s > 0:
            possible_a1s[a1] = s

    for a1, s1 in possible_a1s.items():
        for a2 in get_word(a1).after:
            wa2 = get_word(a2)
            common_of_2_before = set(w2_befores.keys()).intersection(
                set(wa2.before.keys())
            )
            common_of_2_after = set(w2_afters.keys()).intersection(
                set(wa2.after.keys())
            )
            s2 = calc_similarity(
                w2_freq,
                w2_befores,
                w2_afters,
                a2,
                common_of_2_before,
                common_of_2_after,
                get_word,
            )

            if s2 > 0:
                analogies[(a1, a2)] = min(s1, s2)

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
