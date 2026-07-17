from collections import defaultdict

from src.analogy import find_analogies
from src.analysis import analyze_corpus
from src.corpus import assign_train_test, process_txt


def main():
    corp = process_txt("norvig_corpus.txt")
    train, test = assign_train_test(corp, 0.9999)
    word_dict = analyze_corpus(train)
    all_bigrams = {bg for sen in test for bg in zip(sen, sen[1:])}

    result = defaultdict(dict)

    print("Finding analogies")
    nbigrams = len(all_bigrams)
    i = 0
    for bg in all_bigrams:
        for anal, p in find_analogies(word_dict, bg).items():
            result[anal][bg] = p
        i += 1
        print(f"{round(i / nbigrams * 100)}%")

    print("Analogies have been founded")
    print("Writing them out to out.txt")

    with open("out.txt", "w") as f:
        lines = []
        nresult = len(result)
        i = 0
        for anal, pb in result.items():
            lines.append(f"{anal}:\n")
            lines.extend(f"\t{bigram}: {p}\n" for bigram, p in pb.items())
            i += 1
            print(f"{round(i / nresult * 100)}%")
        f.writelines(lines)


if __name__ == "__main__":
    main()
