import pandas as pd
import numpy as np
from model.cleaning import clean_data
from model.syllables import add_syllables_column
from model.homophone import add_homophone_column
from model.has_multiple_pronunciations import has_multiple_pronunciations
from model.difficulty_model  import train_model,save_model,load_model,predict_difficulty
import os
import pandas as pd
folder_path = os.path.join(os.path.dirname(__file__), "datasets", "raw_data")
def get_latest_file(folder_path):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
    files = [f for f in files if os.path.isfile(f)]
    return max(files, key=os.path.getctime)

# Load the CSV
file_path = get_latest_file(folder_path)
df = clean_data(file_path)

# Apply features
df = add_syllables_column(df)
df = add_homophone_column(df)
df = has_multiple_pronunciations(df)
#extracts original name of file and adds complete.csv
base_name = os.path.basename(file_path)            
name, _ = os.path.splitext(base_name)               
output_filename = f"{name}_complete.csv"          
output_path = os.path.join("/home/kevin/repos/word_reader/datasets/complete_data", output_filename)

# Save it
df.to_csv(output_path, index=False)

#load cleaned and featured data for training 
df = pd.read_csv("/home/kevin/repos/word_reader/datasets/complete_data/original_data_frequency_complete.csv")
df["user_difficulty_test"] = np.random.randint(0, 2, size=len(df))
model, scaler = train_model(df)
save_model(model,scaler)
df = predict_difficulty(df,model, scaler)
df.to_csv("data_withpredictions.csv",index= False)

