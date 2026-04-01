# 🧠 Fraudulent Transaction Anomaly Detection System – Architecture

## 📌 Overview

This project is an end-to-end unsupervised machine learning system designed to detect fraudulent or anomalous financial transactions. It integrates machine learning models, backend APIs, a database, and a frontend dashboard into a unified architecture.

The system processes transaction data, assigns anomaly scores, and flags suspicious activities in real time.

---

## 🏗️ High-Level Architecture

```
Frontend (Vue.js)
        │
        ▼
Backend API (FastAPI)
        │
 ┌──────┼──────────┐
 │      │          │
 ▼      ▼          ▼
ML Models   PostgreSQL   Logging System
```

---

## 🔹 Components

### 1. Frontend Layer (Vue.js + Tailwind CSS)

* Displays transaction data and anomaly results
* Provides dashboards with charts and filters
* Sends API requests to backend

---

### 2. Backend Layer (FastAPI)

Responsible for:

* Handling API requests
* Communicating with ML models
* Interacting with the database

Key modules:

* API Routes
* Services (business logic)
* Model Loader
* Database connection

---

### 3. Machine Learning Layer

Implements unsupervised algorithms:

* Isolation Forest (primary)
* DBSCAN (clustering-based anomaly detection)
* Autoencoder (deep learning approach)

Responsibilities:

* Train models
* Generate anomaly scores
* Provide predictions

---

### 4. Database (PostgreSQL)

Stores:

* Transaction records
* Anomaly scores
* Fraud labels
* Logs

---

### 5. Logging & Monitoring

Tracks:

* API requests/responses
* Errors
* System performance

---

## 🔄 Data Flow

### Step-by-Step Flow

1. User submits transaction (via UI or API)
2. Backend receives request
3. Data is preprocessed
4. ML model computes anomaly score
5. Result stored in database
6. Response returned to frontend
7. Dashboard updates with new data

---

## ⚙️ Processing Pipeline

```
Raw Data → Preprocessing → Feature Engineering → Model → Score → Storage → Visualization
```

---

## 🧪 Model Workflow

### Training Phase

* Load dataset
* Clean and normalize data
* Train multiple models
* Save trained models

### Inference Phase

* Load saved model
* Input new transaction
* Compute anomaly score
* Return prediction

---

## 🔐 Security Considerations

* Input validation for all APIs
* Rate limiting (future scope)
* Secure environment variables (.env)

---

## 🚀 Scalability Considerations

* Backend can be containerized using Docker
* Models can be served independently
* Database can be scaled (managed services like Supabase)

---

## 📈 Future Enhancements

* Real-time streaming (Kafka)
* Model retraining pipeline
* Explainability using SHAP
* User authentication system
* Alert notification system

---

## ✅ Summary

This architecture ensures:

* Modularity
* Scalability
* Real-time processing capability
* Clean separation of concerns

The system is designed to simulate real-world fraud detection pipelines used in modern financial systems.
