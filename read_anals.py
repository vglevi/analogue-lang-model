import os
import pickle
import sys


def output_bigrams(anal_path: str):

    bigrams: dict[tuple[str, str], float] = {}

    try:
        with open(f"analogies/{anal_path}", "rb") as f:
            while True:
                try:
                    bg, prop = pickle.load(f)
                    bigrams[bg] = prop
                except EOFError:
                    break

        print(f"Supported bigrams of {anal_path[:-4].replace("_", " ")}:")
        print(bigrams)
        print("===========================\n\n")
    except FileNotFoundError:
        print(f"There is no file: {anal_path}")


def read_anals():
    if len(sys.argv) == 1:

        while True:
            ans = input(
                "Do you want to read the supported bigrams of all analogies? (y / n)  "
            )

            if ans.lower() == "y":
                break
            elif ans.lower() == "n":
                return
            else:
                print("Invalid answer")

        anals = os.scandir("analogies")

        while True:
            anal: str
            try:
                anal = next(anals).name
            except StopIteration:
                break

            output_bigrams(anal)
    else:
        for anal in sys.argv[1:]:
            output_bigrams(anal)


if __name__ == "__main__":
    read_anals()
