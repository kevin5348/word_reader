import pandas as pd
import numpy as np
from model.features.cleaning import clean_data
from model.features.syllables import add_syllables_column
from model.features.homophone import add_homophone_column
from model.features.has_multiple_pronunciations import has_multiple_pronunciations
from model.difficulty_model  import train_model,save_model,load_model,predict_difficulty
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os
import pandas as pd
folder_path = os.path.join(os.path.dirname(__file__), "/home/kevin/repos/word_reader/datasets", "raw_data")
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
def save_latest_file(folder_loaction):
    base_name = os.path.basename(file_path)            
    name, _ = os.path.splitext(base_name)               
    output_filename = folder_loaction + f"{name}"         
    return os.path.join("/home/kevin/repos/word_reader/datasets", output_filename)

# Save it
df.to_csv(save_latest_file("complete_data.csv"), index=False)

folder_path = os.path.join(os.path.dirname(__file__), "/home/kevin/repos/word_reader/datasets", "complete_data")
file_path = get_latest_file(folder_path)
#load cleaned and featured data for training 
df = pd.read_csv(file_path)

# TEMP: assign random difficulty labels (replace with real ones later)

df["user_difficulty_score"] = (
    1 - np.clip(np.log1p(df["count"]) / 10, 0, 1)**2 +
    (df["syllables"] >= 3).astype(int) * 0.2 +
    (df["pronunciation_count"] > 1).astype(int) * 0.2 +
    df["is_homophone"] * 0.3
)



df["user_difficulty_score"] += np.random.normal(0, 0.05, size=len(df))
df["user_difficulty_score"] = np.clip(df["user_difficulty_score"], 0, 1)

# Normalize it to 0–1
df["user_difficulty_score"] = df["user_difficulty_score"] / df["user_difficulty_score"].max()


# Split into 80% train, 20% test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Train on training data
model, scaler = train_model(train_df)
save_model(model, scaler)

# Predict on test data (unseen during training)
test_df = predict_difficulty(test_df, model, scaler)

# Evaluate the model
mse = mean_squared_error(test_df["user_difficulty_score"], test_df["predicted_difficulty"])
print("Mean Squared Error:", mse)

df.to_csv(save_latest_file("finished_model"),index= False)




