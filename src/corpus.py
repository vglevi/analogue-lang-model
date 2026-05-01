import random

def process_txt(file: str) -> list[list[str]]:
    '''
    From a txt file, 
    where each line is a sentence without punctuation
    and all characters are lowercase,
    returns a list of sentences.
    Sentences are represented as list of words.
    '''

    sentences: list[list[str]] = []
    with open(file) as f:
        for sentence in f:
            sentences.append(sentence.strip().split())
    
    return sentences

def assign_train_test(corpus: list[list[str]], rate: float = 0.9) -> tuple[list[list[str]], list[list[str]]]:
    '''
    Shuffles the corpus then splits into a training and a test data based on the given rate.
    The corpus argument should be a list of sentences (a sentence is a list of words).
    The rate argument should be a float between 0 and 1, 
    and it determines the size of the training data.
    The base value of rate is 0.9.
    Returns a tupple containing the training and the test data.
    '''

    if not 0 < rate < 1:
        raise ValueError("Rate should be a float between 0 and 1")

    randomized = random.sample(corpus, len(corpus))
    split_index = round(len(corpus) * rate)

    return randomized[:split_index], randomized[split_index:]
