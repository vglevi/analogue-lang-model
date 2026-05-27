from collections import defaultdict
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from src.analogy import find_analogies
from src.corpus import process_txt, assign_train_test
from src.analysis import WordDict, analyze_corpus

_worker_dict: WordDict | None = None

def _init_worker(word_dict: WordDict) -> None:
    global _worker_dict
    _worker_dict = word_dict

def _find_analogies_worker(bigram: tuple[str, str]):
    return bigram, find_analogies(_worker_dict, bigram)

def main():
    corp = process_txt("norvig_corpus.txt")
    train, test = assign_train_test(corp, 0.9)
    word_dict = analyze_corpus(train)
    all_bigrams = list({bg for sen in test for bg in zip(sen, sen[1:])})

    result = defaultdict(dict)

    with ProcessPoolExecutor(
        max_workers=os.cpu_count(),
        initializer=_init_worker,
        initargs=(word_dict,),
    ) as pool:
        futures = {
            pool.submit(_find_analogies_worker, bg): bg
            for bg in all_bigrams
        }
        for future in as_completed(futures):
            bg, anals = future.result()
            for anal, p in anals.items():
                result[anal][bg] = p
            del futures[future]

    for bg in all_bigrams:
        for anal, p in find_analogies(word_dict, bg).items():
            result[anal][bg] = p

    with open("out.txt", "w") as f:
        for anal, pb in result.items():
            f.write(f"{anal}:\n")
            f.writelines(f"\t{bigram}: {p}\n" for bigram, p in pb.items())


if __name__ == "__main__":
    main()
