from collections import defaultdict
from src.analogy import find_analogies
from src.corpus import process_txt, assign_train_test
from src.analysis import analyze_corpus

def main():
    corp = process_txt("norvig_corpus.txt")
    train, test = assign_train_test(corp, 0.9)
    word_dict = analyze_corpus(train)
    all_bigrams = {bg for sen in test for bg in zip(sen, sen[1:])}

    result = defaultdict(dict)

    for bg in all_bigrams:
        for anal, p in find_analogies(word_dict, bg).items():
            result[anal][bg] = p

    with open("out.txt", "w") as f:
        lines = []
        for anal, pb in result.items():
            lines.append(f"{anal}:\n")
            lines.extend(f"\t{bigram}: {p}\n" for bigram, p in pb.items())
        f.writelines(lines)


if __name__ == "__main__":
    main()
