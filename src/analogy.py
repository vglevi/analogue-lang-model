from src.analysis import WordDict

type Analogies = dict[tuple[str, str], float]


def find_analogies(word_dict: WordDict, bigram: tuple[str, str]) -> Analogies:
    """
    Finds the analogies of bigram in the training data and calculates by how much they increase the probality of the bigram.
    """

    analogies: Analogies = {}
    get_word = word_dict.__getitem__  # avoiding global lookups per call

    b1, b2 = bigram
    w1_bigram = get_word(b1)
    w1_afters = w1_bigram.after
    w1_freq = w1_bigram.freq

    for anal2, freq2 in w1_afters.items():
        p_anal2_given_w1 = freq2 / w1_freq
        w2_anal = get_word(anal2)
        befores_w2_anal = w2_anal.before
        anal2_freq = w2_anal.freq

        for anal1, freq_anal1_given_anal2 in befores_w2_anal.items():
            w1_anal = get_word(anal1)
            freq_b2_given_anal1 = w1_anal.after.get(b2)

            if freq_b2_given_anal1 is not None:
                # Pe(anal2 | b1 _) * Pe(anal1 | _ anal2) * Pe(b2 | anal1 _),
                analogies[(anal1, anal2)] = (
                    p_anal2_given_w1
                    * freq_anal1_given_anal2
                    / anal2_freq
                    * freq_b2_given_anal1
                    / w1_anal.freq
                )

    return analogies
