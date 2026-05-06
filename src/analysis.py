from collections import defaultdict

class Word:
    def __init__(self) -> None:
        self.freq = 0
        self.before: defaultdict[str, int] = defaultdict(int)
        self.after: defaultdict[str, int] = defaultdict(int)

    def __repr__(self) -> str:
        return f"\nFreq = {self.freq}\nBefore: {self.before.items()}\nAfter: {self.after.items()}\n"
