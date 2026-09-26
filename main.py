import os
import pickle
import shutil
from multiprocessing import Pool

from src.analogy import find_analogies
from src.analysis import WordDict, analyze_corpus
from src.corpus import assign_train_test, process_txt
from src.save import bg_to_file_name, save_analogies

_word_dict: WordDict
_a1_cache: dict[str, dict[str, float]] = {}
_sim_cache: dict[tuple[str, str], float] = {}


def _init_worker(word_dict: WordDict) -> None:
    global _word_dict, _a1_cache, _sim_cache
    _word_dict = word_dict
    _a1_cache = {}
    _sim_cache = {}


def _process_bigram(bg: tuple[str, str]) -> tuple[str, str]:
    analogies = find_analogies(_word_dict, bg, _a1_cache, _sim_cache)
    save_analogies(bg, analogies)
    return bg


def main():
    corp = process_txt("norvig_corpus.txt")
    train, test = assign_train_test(corp, 0.9)
    word_dict = analyze_corpus(train)
    all_test_bigrams = sorted(
        {bg for sen in test for bg in zip(sen, sen[1:])}, key=lambda bg: bg[0]
    )

    try:
        shutil.rmtree("bigrams")
    except FileNotFoundError:
        pass

    print("Creating directory bigrams")
    os.mkdir("bigrams")

    print("Finding analogies")
    nbigrams = len(all_test_bigrams)

    ncores = os.cpu_count() or 1
    chunksize = max(1, nbigrams // (ncores * 8))

    with Pool(
        processes=ncores, initializer=_init_worker, initargs=(word_dict,)
    ) as pool:
        for i, _ in enumerate(
            pool.imap_unordered(_process_bigram, all_test_bigrams, chunksize=chunksize),
            start=1,
        ):
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


if __name__ == "__main__":
    main()
