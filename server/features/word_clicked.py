import pandas as pd

df = pd.read_csv("server/datasets/original_data_frequency_complete.csv")

def when_word_clicked(word):
    result =df[df["word"]==word.str.lower()]["user_difficulty_score"]
    
