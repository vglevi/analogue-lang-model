from collections import defaultdict
from collections.abc import Callable

from src.analysis import Word, WordDict

type Analogies = dict[tuple[str, str], float]


def build_a1_cache(b1: str, get_word: Callable[[str], Word]) -> dict[str, float]:
    w1 = get_word(b1)

    a1_sl_d: defaultdict[str, float] = defaultdict(float)
    for x1, x1b1_freq in w1.before.items():
        wx1 = get_word(x1)
        wx1_afters = wx1.after
        wx1_freq = wx1.freq
        for a1, x1a1_freq in wx1_afters.items():
            wa1 = get_word(a1)
            a1_sl_d[a1] += min(x1a1_freq / wa1.freq, x1b1_freq / wx1_freq)

    a1_sr_d: defaultdict[str, float] = defaultdict(float)
    for y1, b1y1_freq in w1.after.items():
        wy1 = get_word(y1)
        wy1_befores = wy1.before
        wy1_freq = wy1.freq
        for a1, a1y1_freq in wy1_befores.items():
            wa1 = get_word(a1)
            a1_sr_d[a1] += min(a1y1_freq / wa1.freq, b1y1_freq / wy1_freq)

    return {a1: s for a1, sl in a1_sl_d.items() if (s := min(sl, a1_sr_d[a1])) > 0}


def find_analogies(
    word_dict: WordDict,
    bigram: tuple[str, str],
    a1_cache: dict[str, dict[str, float]],
    sim_cache: dict[tuple[str, str], float],
) -> Analogies:
    """
    Finds the analogies of bigram in the training data and calculates by how much they increase the probality of the bigram.
    """

    analogies: Analogies = {}
    get_word = word_dict.__getitem__  # avoiding global lookups per call
    b1, b2 = bigram
    w2 = get_word(b2)

    if b1 not in a1_cache:
        a1_cache[b1] = build_a1_cache(b1, get_word)
    possible_a1s = a1_cache[b1]

    for a1, s1 in possible_a1s.items():
        for a2 in list(
            get_word(a1).after
        ):  # pass by value instead of reference so dict size increase wont affect the cycle
            key = (b2, a2)
            if key not in sim_cache:
                wa2 = get_word(a2)
                sim_cache[key] = calc_similarity(b2, w2.before, w2.after, wa2, get_word)
            s2 = sim_cache[key]
            if s2 > 0:
                analogies[(a1, a2)] = min(s1, s2)

    return analogies


def calc_similarity(
    b: str,
    word_befores: defaultdict[str, int],
    word_afters: defaultdict[str, int],
    wanal: Word,
    get_word: Callable[[str], Word],
) -> float:
    sl: float = 0.0
    sr: float = 0.0

    wanal_befores = wanal.before
    wanal_afters = wanal.after
    wanal_freq = wanal.freq

    if len(word_befores) <= len(wanal_befores):
        for x in word_befores:
            wx = get_word(x)
            sl += min(wanal_befores[x] / wanal_freq, wx.after[b] / wx.freq)
    else:
        for x, xanal_freq in wanal_befores.items():
            wx = get_word(x)
            sl += min(xanal_freq / wanal_freq, wx.after[b] / wx.freq)

    if len(word_afters) <= len(wanal_afters):
        for y in word_afters:
            wy = get_word(y)
            sr += min(wanal_afters[y] / wanal_freq, wy.before[b] / wy.freq)
    else:
        for y, analy_freq in wanal_afters.items():
            wy = get_word(y)
            sr += min(analy_freq / wanal_freq, wy.before[b] / wy.freq)

    return min(sl, sr)
