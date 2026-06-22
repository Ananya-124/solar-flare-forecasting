import os

# Define the directory structure
structure = {
    "models": ["tft_model.ckpt", "scaler.pkl"],
    "src": {
        "preprocess": ["process_solexs.py", "process_hel1os.py", "merge_data.py"],
        "features": ["create_features.py"],
        "training": ["prepare_tft.py", "train_tft.py"],
        "inference": ["predict.py"],
        "utils": ["helpers.py"]
    },
    "dashboard": ["app.py"]
}

# Root level files
root_files = ["src/config.py", "requirements.txt", "main.py"]

def create_structure(base_path="."):
    # Create subdirectories and files
    for folder, contents in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        if isinstance(contents, list):
            for file in contents:
                file_path = os.path.join(folder_path, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        f.write(f"# Placeholder for {file}")
        elif isinstance(contents, dict):
            for subfolder, files in contents.items():
                subfolder_path = os.path.join(folder_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)
                for file in files:
                    file_path = os.path.join(subfolder_path, file)
                    if not os.path.exists(file_path):
                        with open(file_path, 'w') as f:
                            f.write(f"# Placeholder for {file}")

    # Create root files
    for file in root_files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write(f"# Placeholder for {file}")

if __name__ == "__main__":
    create_structure()
    print("Project structure initialized successfully.")