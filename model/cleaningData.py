import math
import pandas as pd
#opens dataset and gets length of set
with open("datasets/frequency/frequency1", "r") as f:
    lines = f.readlines()
# splits data into frequency word and int value plus gets rid of white spaces
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

#turns data into a dataFrame and logs the data.Also turns the data into a csv file
df = pd.DataFrame(list(word_counts.items()), columns=["word", "count"])
df["log_count"] = df["count"].apply(math.log)
df.to_csv("datasets/frequency/word_frequencies.csv", index=False)



