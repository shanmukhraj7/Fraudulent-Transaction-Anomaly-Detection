from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    time_val: float = Field(..., alias="time")
    amount:   float = Field(..., gt=0)

    v1:  float = 0.0; v2:  float = 0.0; v3:  float = 0.0
    v4:  float = 0.0; v5:  float = 0.0; v6:  float = 0.0
    v7:  float = 0.0; v8:  float = 0.0; v9:  float = 0.0
    v10: float = 0.0; v11: float = 0.0; v12: float = 0.0
    v13: float = 0.0; v14: float = 0.0; v15: float = 0.0
    v16: float = 0.0; v17: float = 0.0; v18: float = 0.0
    v19: float = 0.0; v20: float = 0.0; v21: float = 0.0
    v22: float = 0.0; v23: float = 0.0; v24: float = 0.0
    v25: float = 0.0; v26: float = 0.0; v27: float = 0.0
    v28: float = 0.0

    model_config = {"populate_by_name": True}


class PredictResponse(BaseModel):
    transaction_id: UUID
    anomaly_score:  float
    is_fraud:       bool
    confidence:     Optional[float] = None
    model_name:     str


class HealthResponse(BaseModel):
    status:   str
    database: str
    model:    str