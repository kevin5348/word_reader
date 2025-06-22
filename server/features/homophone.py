import pandas as pd
import nltk
from nltk.corpus import cmudict
from collections import defaultdict




pronounce = cmudict.dict()

def add_homophone_column(df):
#Build a set of valid/common words 
    valid_words = set(df["word"].str.lower())

# Build pronunciation groups
    pronounce_groups = defaultdict(list)

    for word in valid_words:
        if word in pronounce and pronounce[word]:
            pron_key = tuple(pronounce[word][0])
            pronounce_groups[pron_key].append(word)

# Build homophone set from valid groups only
    homophone_set = set()
    for group in pronounce_groups.values():
        if len(group) > 1:
            homophone_set.update(group)

# Fast lookup function
    def is_homophone(word):
        return word.lower() in homophone_set


    df["is_homophone"] = df["word"].apply(is_homophone)
    return df


    

