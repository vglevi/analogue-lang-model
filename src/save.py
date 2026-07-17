import pickle

from src.analogy import Analogies


def save_analogies(bg: tuple[str, str], analogies: Analogies) -> bool:
    """
    Saves the 10 most probability increasing anologies in a pickle file named by the bigram.
    """

    with open(f"bigrams/{bg[0]}_{bg[1]}.pkl", "wb") as f:
        pickle.dump(
            sorted(analogies.items(), key=lambda x: x[1], reverse=True)[:10],
            f,
            pickle.HIGHEST_PROTOCOL,
        )

    return True
