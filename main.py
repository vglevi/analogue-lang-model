import os
import pickle
import shutil

from src.analogy import find_analogies
from src.analysis import analyze_corpus
from src.corpus import assign_train_test, process_txt
from src.save import bg_to_file_name, save_analogies


def main():
    corp = process_txt("norvig_corpus.txt")
    train, test = assign_train_test(corp, 0.9)
    word_dict = analyze_corpus(train)
    all_bigrams = {bg for sen in test for bg in zip(sen, sen[1:])}

    try:
        shutil.rmtree("bigrams")
    except FileNotFoundError:
        pass

    print("Creating directory bigrams")
    os.mkdir("bigrams")

    print("Finding analogies")
    nbigrams = len(all_bigrams)
    i = 0
    for bg in all_bigrams:
        save_analogies(bg, find_analogies(word_dict, bg))
        i += 1
        print(f"\rProcessed {i}/{nbigrams} ({i / nbigrams:.1%})", end="", flush=True)

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
