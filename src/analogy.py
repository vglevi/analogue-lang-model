from src.analysis import WordDict

type Analogies = dict[tuple[str, str], float]

def find_analogies(word_dict: WordDict, bigram: tuple[str, str]):
    analogies: Analogies = {}
    w1_bigram = word_dict[bigram[0]]
    w1_afters = w1_bigram.after

    for anal2, freq2 in w1_afters.items():
        w2_anal = word_dict[anal2]
        befores_w2_anal = w2_anal.before

        for anal1, freq1 in befores_w2_anal.items():
            w1_anal = word_dict[anal1]
            freq3 = w1_anal.after.get(bigram[1])

            if freq3 is not None:
                # Pe(anal1 | w1 _) * Pe(anal1 | _ anal2) * Pe(w2 | anal2 _),
                analogies[(anal1, anal2)] = (freq2 / w1_bigram.freq
                                             * freq1 / w2_anal.freq
                                             * freq3 / w1_anal.freq)

    return analogies

