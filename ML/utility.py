import pickle
from pathlib import Path

def save_model(model, filepath):
    # saves the model to disk
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        pickle.dump(model, f)
    print(f"[utility] Model saved to {filepath}")

def load_model(filepath):
    # loading a model from the disk
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"[utility] Model not found at {filepath}")
    with open(filepath, "rb") as f:
        model = pickle.load(f)
    print(f"[utility] Model loaded from {filepath}")
    return model
