import os
import pickle
import sys


def read():
    print("Im reading")
    print(", ".join(sys.argv))

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

            with open(f"bigrams/{bg}", "rb") as f:
                data = pickle.load(f)

            print(f"Analogies of {bg}:")
            print(data)
            print("===========================")


if __name__ == "__main__":
    read()
