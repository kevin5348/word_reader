import pandas as pd
import nltk
from nltk.corpus import cmudict
from collections import defaultdict
import os


nltk.download("cmudict")
pronounce = cmudict.dict()

#Get path to CSV relative 
script_dir = os.path.dirname(__file__)
csv_path = os.path.join(script_dir, "datasets/word_frequencies.csv")

#Load word frequency data
df = pd.read_csv(csv_path)

#get rid of null and float values 
df = df.dropna(subset=["word"])
df = df[df["word"].apply(lambda x: isinstance(x, str))]

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
output_path = os.path.join(script_dir, "datasets/word_frequencies_with_homophones.csv")
df.to_csv(output_path, index=False)


    

