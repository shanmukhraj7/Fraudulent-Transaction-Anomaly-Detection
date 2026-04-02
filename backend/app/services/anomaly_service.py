from __future__ import annotations

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from ..api.schemas import TransactionInput, PredictResponse
from ..db.models import Transaction, Prediction
from .model_loader import load_model

_FEATURE_COLS = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]


def _build_feature_row(txn: TransactionInput) -> pd.DataFrame:
    row = {
        "Time":   txn.time_val,
        "Amount": txn.amount,
        **{f"V{i}": getattr(txn, f"v{i}") for i in range(1, 29)},
    }
    return pd.DataFrame([row], columns=_FEATURE_COLS)


def _normalise_score(raw_score: float) -> float:
    clipped = float(np.clip(-raw_score, -0.5, 0.5))
    return round((clipped + 0.5), 4)


def predict_and_store(txn_input: TransactionInput, db: Session) -> PredictResponse:
    # 1. Save transaction
    txn_row = Transaction(
        time_val=txn_input.time_val,
        amount=txn_input.amount,
        **{f"v{i}": getattr(txn_input, f"v{i}") for i in range(1, 29)},
    )
    db.add(txn_row)
    db.flush()

    # 2. Predict
    model = load_model()
    X = _build_feature_row(txn_input)
    raw_label: int  = model.predict(X)[0]
    decision: float = model.decision_function(X)[0]
    is_fraud:  bool  = raw_label == -1
    confidence: float = _normalise_score(decision)

    # 3. Save prediction
    pred_row = Prediction(
        transaction_id=txn_row.id,
        model_name="isolation_forest",
        anomaly_score=round(float(decision), 6),
        is_fraud=is_fraud,
        confidence=confidence,
    )
    db.add(pred_row)
    db.commit()

    return PredictResponse(
        transaction_id=txn_row.id,
        anomaly_score=round(float(decision), 6),
        is_fraud=is_fraud,
        confidence=confidence,
        model_name="isolation_forest",
    )


def get_all_transactions(db: Session, limit: int = 100, offset: int = 0):
    from sqlalchemy import text
    rows = db.execute(
        text("SELECT * FROM transactions_with_predictions ORDER BY created_at DESC LIMIT :lim OFFSET :off"),
        {"lim": limit, "off": offset},
    ).mappings().all()
    return [dict(r) for r in rows]


def get_transaction_by_id(txn_id: str, db: Session):
    from sqlalchemy import text
    row = db.execute(
        text("SELECT * FROM transactions_with_predictions WHERE id = :id"),
        {"id": txn_id},
    ).mappings().first()
    return dict(row) if row else None