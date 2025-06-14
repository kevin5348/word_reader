import math
import pandas as pd
with open("/home/kevin/repos/word_reader/model/datasets/freqency/frequency1", "r") as f:
    lines = f.readlines()

    word_counts = {}
    for line in lines :
        word, count = line.split()
        word_counts[word] = int (count)

        limited_word_counts = dict(list(word_counts.items())[:1000])
        df = pd.DataFrame(list(limited_word_counts.items()), columns=["word", "count"])
      

    
    for i in range(10):
        print(lines[i])
