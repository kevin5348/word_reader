import math
import pandas as pd

#opens dataset and gets length of set

# splits data into frequency word and int value plus gets rid of white spaces
def clean_data(file):
    with open(file, "r") as f:
        lines = f.readlines()
    word_counts = {}
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        word, count = parts
        try:
            word_counts[word] = int(count)
        except ValueError:
            continue

#turns data into a dataFrame
    df = pd.DataFrame(list(word_counts.items()), columns=["word", "count"])

#get rid of null and float values 
    df = df.dropna(subset=["word"])
    df = df[df["word"].apply(lambda x: isinstance(x, str))]

#adds log and length columns
    df["log_count"] = df["count"].apply(math.log)
    df["length"] = df["word"].apply(len)
#returns back to main
    return df



