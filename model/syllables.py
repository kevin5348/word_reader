from nltk.corpus import cmudict
pronounce = cmudict.dict()

def count_syllables(word):
    if not isinstance(word, str):
        return 0  
    word = word.lower()
    if word in pronounce:
        phonemes = pronounce[word][0]
        return sum(1 for p in phonemes if p[-1].isdigit())
    return 0


def add_syllables_column(df):
    df["syllables"] = df["word"].apply(count_syllables)
    return df