import datetime
import os
import pickle
import shutil
from functools import lru_cache
from itertools import groupby
from multiprocessing import Pool

from src.analogy import build_a1_cache, calc_similarity
from src.analysis import WordDict, analyze_corpus
from src.corpus import assign_train_test, process_txt
from src.save import bg_to_file_name, save_analogies

_word_dict: WordDict
_a1_cache: dict[str, dict[str, float]] = {}
_sim_cache: dict[tuple[str, str], float] = {}


@lru_cache(maxsize=200000)
def calc_similarity_cached(b2: str, a2: str) -> float:
    get_word = _word_dict.__getitem__
    w2 = get_word(b2)
    wanal = get_word(a2)
    return calc_similarity(b2, w2.before, w2.after, wanal, get_word)


def _init_worker(word_dict: WordDict) -> None:
    global _word_dict, _a1_cache, _sim_cache
    _word_dict = word_dict
    _a1_cache = {}
    _sim_cache = {}


def make_groups(sorted_bigrams: list[tuple[str, str]]):
    return [list(g) for _, g in groupby(sorted_bigrams, key=lambda bg: bg[0])]


def _process_group(bigram_group: list[tuple[str, str]]):
    b1 = bigram_group[0][0]
    possible_a1s = build_a1_cache(b1, _word_dict.__getitem__)
    for bg in bigram_group:
        b1, b2 = bg
        analogies = {}
        for a1, s1 in possible_a1s.items():
            for a2 in list(_word_dict[a1].after):
                s2 = calc_similarity_cached(b2, a2)
                if s2 > 0:
                    analogies[(a1, a2)] = min(s1, s2)
        save_analogies(bg, analogies)
    return len(bigram_group)


def main():
    corp = process_txt("norvig_corpus.txt")
    train, test = assign_train_test(corp, 0.9)
    word_dict = analyze_corpus(train)
    all_test_bigrams = sorted(
        {bg for sen in test for bg in zip(sen, sen[1:])}, key=lambda bg: bg[0]
    )[:10000]

    try:
        shutil.rmtree("bigrams")
    except FileNotFoundError:
        pass

    print("Creating directory bigrams")
    os.mkdir("bigrams")

    print("Finding analogies")
    nbigrams = len(all_test_bigrams)

    ncores = os.cpu_count() or 1

    groups = make_groups(all_test_bigrams)

    with Pool(
        processes=ncores, initializer=_init_worker, initargs=(word_dict,)
    ) as pool:
        i = 0
        for n in pool.imap_unordered(
            _process_group, groups, chunksize=max(1, len(groups))
        ):
            i += n
            print(
                f"\rProcessed {i}/{nbigrams} ({i / nbigrams:.1%})", end="", flush=True
            )

    print()

    try:
        shutil.rmtree("analogies")
    except FileNotFoundError:
        pass

    print("Creating directory analogies")
    os.mkdir("analogies")

    bg_paths = os.listdir("bigrams/")
    npaths = len(bg_paths)
    i = 0
    for bg_path in bg_paths:
        with open(f"bigrams/{bg_path}", "rb") as bg_file:
            data: list = pickle.load(bg_file)
            bg: tuple[str, str] = data[0]
            analogies: dict[tuple[str, str], float] = dict(data[1])
            for anal in analogies:
                with open(f"analogies/{bg_to_file_name(anal)}", "ab") as anal_file:
                    pickle.dump(
                        (bg, analogies[anal]), anal_file, pickle.HIGHEST_PROTOCOL
                    )
        i += 1
        print(f"\rProcessed {i}/{npaths} ({i / npaths:.1%})", end="", flush=True)

    print(f"Completed at: {datetime.datetime.now().time()}")


if __name__ == "__main__":
    main()
