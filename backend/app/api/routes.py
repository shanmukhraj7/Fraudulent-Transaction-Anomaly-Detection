from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db.database import get_db, ping_database
from ..services.anomaly_service import get_all_transactions, get_transaction_by_id, predict_and_store
from ..services.model_loader import load_model
from .schemas import HealthResponse, PredictResponse, TransactionInput

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health_check():
    db_ok = ping_database()
    model_ok = True
    try:
        load_model()
    except Exception:
        model_ok = False
    return HealthResponse(
        status="ok" if (db_ok and model_ok) else "degraded",
        database="connected" if db_ok else "unreachable",
        model="loaded" if model_ok else "unavailable",
    )


@router.post("/predict", response_model=PredictResponse, status_code=201, tags=["ml"])
def predict(payload: TransactionInput, db: Session = Depends(get_db)):
    try:
        return predict_and_store(payload, db)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/transactions", tags=["transactions"])
def list_transactions(
    limit:  int = Query(50, ge=1, le=500),
    offset: int = Query(0,  ge=0),
    db: Session = Depends(get_db),
):
    return get_all_transactions(db, limit=limit, offset=offset)


@router.get("/transactions/{transaction_id}", tags=["transactions"])
def get_transaction(transaction_id: UUID, db: Session = Depends(get_db)):
    row = get_transaction_by_id(str(transaction_id), db)
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return row


@router.get("/explain/{transaction_id}", tags=["ml"])
def explain(transaction_id: UUID, db: Session = Depends(get_db)):
    row = get_transaction_by_id(str(transaction_id), db)
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {
        "transaction_id": str(transaction_id),
        "note": "SHAP explainability not yet configured.",
        "is_fraud": row.get("is_fraud"),
        "anomaly_score": row.get("anomaly_score"),
    }