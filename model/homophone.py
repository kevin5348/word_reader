import pandas as pd 
import nltk
from nltk.corpus import cmudict




nltk.download('cmudict')

pronounce = cmudict.dict()

def has_homophone(word):
    if not isinstance(word, str):
        return False
    word = word.lower()
    try:
        pronunciation = pronounce[word]
        for other_word in pronounce:
            if other_word.lower() != word and pronounce[other_word]==pronounce[word]:
                return True
        return False
    except KeyError:
        return None
    
df = pd.read_csv("datasets/frequency/word_frequencies.csv")
df["is_homophone"] = df["word"].apply(has_homophone)
df.to_csv("datasets/word_frequencies_with_homophones.csv", index=False)
