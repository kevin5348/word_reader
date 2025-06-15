import pandas as pd
from model.syllable import add_syllable_column
from model.homophone import add_homophone_column

# Load the CSV
df = pd.read_csv("datasets/word_data.csv")

# Apply features
df = add_syllable_column(df)
df = add_homophone_column(df)

# Save the result
df.to_csv("datasets/enriched_word_data.csv", index=False)
