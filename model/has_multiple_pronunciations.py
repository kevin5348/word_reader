import pandas as pd
import nltk
from nltk.corpus import cmudict
from collections import defaultdict
pronounce = cmudict.dict()
def count_pronunciations(word):
    word = word.lower()
    if word in pronounce and pronounce[word]:
        return len(pronounce[word])
    return 0

def has_multiple_pronunciations(df):
    df["pronunciation_count"] = df["word"].apply(count_pronunciations)
    return df

           