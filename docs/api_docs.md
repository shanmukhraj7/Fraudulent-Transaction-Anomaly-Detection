# 📡 Fraud Detection API Documentation

## 📌 Base URL

```
http://localhost:8000
```

---

## 🔹 1. Predict Anomaly

### Endpoint

```
POST /predict
```

### Description

Predicts whether a transaction is anomalous and returns an anomaly score.

---

### Request Body

```json
{
  "amount": 1200.50,
  "time": 34567,
  "feature_1": 0.23,
  "feature_2": -1.45
}
```

---

### Response

```json
{
  "anomaly_score": 0.92,
  "is_fraud": true
}
```

---

### Status Codes

* 200 → Success
* 400 → Invalid input
* 500 → Server error

---

## 🔹 2. Get All Transactions

### Endpoint

```
GET /transactions
```

### Description

Returns all stored transactions with anomaly scores.

---

### Response

```json
[
  {
    "id": 1,
    "amount": 500,
    "anomaly_score": 0.12,
    "is_fraud": false
  }
]
```

---

## 🔹 3. Get Transaction by ID

### Endpoint

```
GET /transactions/{id}
```

---

### Response

```json
{
  "id": 1,
  "amount": 500,
  "anomaly_score": 0.12,
  "is_fraud": false
}
```

---

## 🔹 4. Explain Prediction

### Endpoint

```
GET /explain/{id}
```

### Description

Provides explanation for why a transaction was flagged.

---

### Response

```json
{
  "transaction_id": 1,
  "important_features": [
    {"feature": "amount", "impact": 0.7},
    {"feature": "time", "impact": 0.2}
  ]
}
```

---

## 🔹 5. Health Check

### Endpoint

```
GET /health
```

---

### Response

```json
{
  "status": "ok"
}
```

---

## 🔐 Error Format

```json
{
  "error": "Invalid input data"
}
```

---

## 📦 Request Validation

* All inputs are validated using Pydantic schemas
* Missing or incorrect fields return 400 error

---

## 🚀 Future API Enhancements

* Authentication (JWT)
* Rate limiting
* Batch prediction endpoint
* Real-time streaming API

---

## ✅ Summary

This API layer:

* Provides real-time anomaly detection
* Acts as a bridge between frontend and ML models
* Ensures scalability and modularity

It is designed following REST principles and can be easily extended for production use.
