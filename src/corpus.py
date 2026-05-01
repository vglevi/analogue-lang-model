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
