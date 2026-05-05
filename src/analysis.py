from collections import defaultdict

class Word:
    def __init__(self) -> None:
        self.freq = 0
        self.before: defaultdict[str, int] = defaultdict(int)
        self.after: defaultdict[str, int] = defaultdict(int)
