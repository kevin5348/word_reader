from features.cleaning import clean_data
from features.syllables import add_syllables_column
from features.homophones import add_homophone_column
from features.has_multiple_pronunciations import has_multiple_pronunciations

def preprocess_dataframe(df):
    df = clean_data(df)
    df = add_syllables_column(df)
    df = add_homophone_column(df)
    df = has_multiple_pronunciations(df)
    return df
