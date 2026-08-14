import os
import pickle
import sys


def output_anal(bg_path: str):
    try:
        with open(f"bigrams/{bg_path}", "rb") as f:
            data = pickle.load(f)

        print(f"Analogies of {bg_path[:-4].replace("_", " ")}:")
        print(data)
        print("===========================\n\n")
    except FileNotFoundError:
        print(f"There is no file: {bg_path}")


def read_bigrams():
    if len(sys.argv) == 1:

        while True:
            ans = input("Do you want to read the analogies of all bigrams? (y / n)  ")

            if ans.lower() == "y":
                break
            elif ans.lower() == "n":
                return
            else:
                print("Invalid answer")

        bigrams = os.scandir("bigrams")

        while True:
            bg: str
            try:
                bg = next(bigrams).name
            except StopIteration:
                break

            output_anal(bg)

    else:
        for bg in sys.argv[1:]:
            output_anal(bg)


if __name__ == "__main__":
    read_bigrams()
