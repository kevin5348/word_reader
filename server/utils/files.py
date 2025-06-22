import os

def get_latest_file(folder_path):
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return max(files, key=os.path.getctime)
