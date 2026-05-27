from collections import defaultdict
import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from src.analogy import find_analogies
from src.corpus import process_txt, assign_train_test
from src.analysis import WordDict, analyze_corpus

_worker_dict: WordDict | None = None

def _init_worker(word_dict: WordDict):
    global _worker_dict
    _worker_dict = word_dict

def _find_analogies_worker(bigram: tuple[str, str]):
    return bigram, find_analogies(_worker_dict, bigram)

def main():
    corp = process_txt("norvig_corpus.txt")
    train, test = assign_train_test(corp, 0.999)
    word_dict = analyze_corpus(train)
    all_bigrams = list({bg for sen in test for bg in zip(sen, sen[1:])})

    workers = os.cpu_count() or 4

    ctx = multiprocessing.get_context("spawn")

    with ProcessPoolExecutor(
            max_workers=workers,
            mp_context=ctx,
            initializer=_init_worker,
            initargs=(word_dict,),
            ) as pool:
        cache = dict(
                    pool.map(_find_analogies_worker, all_bigrams, chunksize=64)
                )

    result = defaultdict(dict)

    for bigram, anals in cache.items():
        for anal, p in anals.items():
            result[anal][bigram] = p

    with open("out.txt", "w") as f:
        for anal, pb in result.items():
            f.write(f"{anal}:\n")
            f.writelines(f"\t{bigram}: {p}\n" for bigram, p in pb.items())

if __name__ == "__main__":
    main()
