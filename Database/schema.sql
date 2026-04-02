-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS transactions (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    time_val      FLOAT NOT NULL,
    amount        FLOAT NOT NULL,
    v1            FLOAT, v2  FLOAT, v3  FLOAT, v4  FLOAT,
    v5            FLOAT, v6  FLOAT, v7  FLOAT, v8  FLOAT,
    v9            FLOAT, v10 FLOAT, v11 FLOAT, v12 FLOAT,
    v13           FLOAT, v14 FLOAT, v15 FLOAT, v16 FLOAT,
    v17           FLOAT, v18 FLOAT, v19 FLOAT, v20 FLOAT,
    v21           FLOAT, v22 FLOAT, v23 FLOAT, v24 FLOAT,
    v25           FLOAT, v26 FLOAT, v27 FLOAT, v28 FLOAT,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS predictions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id  UUID NOT NULL REFERENCES transactions(id) ON DELETE CASCADE,
    model_name      TEXT NOT NULL,
    anomaly_score   FLOAT,
    is_fraud        BOOLEAN NOT NULL DEFAULT FALSE,
    confidence      FLOAT,
    predicted_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    endpoint     TEXT NOT NULL,
    method       TEXT NOT NULL,
    status_code  INT,
    duration_ms  FLOAT,
    error_msg    TEXT,
    logged_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_predictions_transaction ON predictions(transaction_id);
CREATE INDEX IF NOT EXISTS idx_predictions_is_fraud    ON predictions(is_fraud);
CREATE INDEX IF NOT EXISTS idx_transactions_created    ON transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_logged       ON audit_logs(logged_at DESC);

CREATE OR REPLACE VIEW transactions_with_predictions AS
SELECT
    t.id, t.amount, t.time_val, t.created_at,
    p.model_name, p.anomaly_score, p.is_fraud, p.confidence, p.predicted_at
FROM transactions t
LEFT JOIN predictions p ON p.transaction_id = t.id;