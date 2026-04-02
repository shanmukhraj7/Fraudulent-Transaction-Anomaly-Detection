import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from .database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time_val   = Column(Float, nullable=False)
    amount     = Column(Float, nullable=False)

    v1  = Column(Float); v2  = Column(Float); v3  = Column(Float)
    v4  = Column(Float); v5  = Column(Float); v6  = Column(Float)
    v7  = Column(Float); v8  = Column(Float); v9  = Column(Float)
    v10 = Column(Float); v11 = Column(Float); v12 = Column(Float)
    v13 = Column(Float); v14 = Column(Float); v15 = Column(Float)
    v16 = Column(Float); v17 = Column(Float); v18 = Column(Float)
    v19 = Column(Float); v20 = Column(Float); v21 = Column(Float)
    v22 = Column(Float); v23 = Column(Float); v24 = Column(Float)
    v25 = Column(Float); v26 = Column(Float); v27 = Column(Float)
    v28 = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    predictions = relationship("Prediction", back_populates="transaction", cascade="all, delete")

    def to_feature_dict(self) -> dict:
        return {
            "Time": self.time_val,
            "Amount": self.amount,
            **{f"V{i}": getattr(self, f"v{i}") for i in range(1, 29)},
        }


class Prediction(Base):
    __tablename__ = "predictions"

    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False)
    model_name     = Column(Text, nullable=False)
    anomaly_score  = Column(Float)
    is_fraud       = Column(Boolean, nullable=False, default=False)
    confidence     = Column(Float)
    predicted_at   = Column(DateTime(timezone=True), server_default=func.now())

    transaction = relationship("Transaction", back_populates="predictions")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    endpoint    = Column(Text, nullable=False)
    method      = Column(Text, nullable=False)
    status_code = Column(Integer)
    duration_ms = Column(Float)
    error_msg   = Column(Text)
    logged_at   = Column(DateTime(timezone=True), server_default=func.now())