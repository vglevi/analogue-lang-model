from src.analysis import WordDict

type Analogies = dict[tuple[str, str], float]

def find_analogies(word_dict: WordDict, bigram: tuple[str, str]):

    analogies: Analogies = {}

    wbefore_bigram = word_dict[bigram[0]]
    wafter_bigram = word_dict[bigram[1]]

    for after_anal in wbefore_bigram.after:
        wafter_anal = word_dict[after_anal]

        for before_anal in wafter_anal.before:

            wbefore_anal = word_dict[before_anal]

            if bigram[1] in wbefore_anal.after:
                # Pe(day | strange _) * Pe(good | _ day) * Pe(weather | good _),
                analogies[(before_anal, after_anal)] = (wbefore_bigram.after[after_anal] / wbefore_bigram.freq
                                                        * wafter_anal.before[before_anal] / wafter_anal.freq
                                                        * wbefore_anal.after[bigram[1]] / wbefore_anal.freq)
    
    return analogies

