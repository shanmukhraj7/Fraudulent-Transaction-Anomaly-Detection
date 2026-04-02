import os
import pickle
from pathlib import Path
from typing import Optional

from sklearn.ensemble import IsolationForest

_MODEL_PATH = Path(os.getenv("MODEL_PATH", "ml/models/isolation_forest.pkl"))
_model: Optional[IsolationForest] = None


def load_model() -> IsolationForest:
    global _model
    if _model is not None:
        return _model

    if _MODEL_PATH.exists():
        with open(_MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        print(f"[ModelLoader] Loaded model from {_MODEL_PATH}")
    else:
        print(f"[ModelLoader] No saved model at {_MODEL_PATH}. Using default untrained model.")
        _model = IsolationForest(n_estimators=100, contamination=0.005, random_state=42)

    return _model


def save_model(model: IsolationForest) -> None:
    global _model
    _MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    _model = model
    print(f"[ModelLoader] Model saved to {_MODEL_PATH}")


def invalidate_cache() -> None:
    global _model
    _model = None