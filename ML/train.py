import os
import sys
import pickle
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from preprocessing import load_dataset, preprocessing_data
from model_isolation_forest import train_isolation_forest

MODEL_DIR  = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "isolation_forest.pkl"
DATA_PATH  = Path(__file__).parent / "data" / "creditcard.csv"


def run_training(data_path: Path = DATA_PATH) -> None:
    if not data_path.exists():
        print(f"[train] Dataset not found at {data_path}. Aborting.")
        sys.exit(1)

    print(f"[train] Loading dataset...")
    df = load_dataset(str(data_path))
    X, y = preprocessing_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[train] Train: {len(X_train)}  Test: {len(X_test)}")

    print("[train] Training Isolation Forest...")
    model = train_isolation_forest(X_train)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"[train] Model saved → {MODEL_PATH}")

    from sklearn.metrics import classification_report
    from model_isolation_forest import predict as if_predict
    y_pred = if_predict(model, X_test)
    print(classification_report(y_test, y_pred))

    _log_training_run(len(X_train), len(X_test))


def _log_training_run(n_train: int, n_test: int) -> None:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        import psycopg2
        conn_str = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:Shanmukh1430@db.bfcqpvzrycxkrgoyvmjm.supabase.co:5432/postgres",
        )
        with psycopg2.connect(conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO audit_logs (endpoint, method, status_code, duration_ms) VALUES (%s, %s, %s, %s)",
                    (f"/train [n_train={n_train}, n_test={n_test}]", "SCRIPT", 200, 0.0),
                )
        print("[train] Run logged to Supabase.")
    except Exception as exc:
        print(f"[train] Could not log to Supabase (non-fatal): {exc}")


if __name__ == "__main__":
    run_training()


## `backend/requirements.txt`
# fastapi==0.115.0
# uvicorn[standard]==0.30.6
# python-multipart==0.0.9
# sqlalchemy==2.0.35
# psycopg2-binary==2.9.9
# python-dotenv==1.0.1
# pydantic==2.9.2
# scikit-learn==1.5.2
# numpy==1.26.4
# pandas==2.2.3
# httpx==0.27.2