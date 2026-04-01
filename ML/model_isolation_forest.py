from sklearn.ensemble import IsolationForest

def train_isolation_forest(X_train):
    model = IsolationForest(
        n_estimators = 100,
        contamination = 0.005,
        random_state = 42
    )

    model.fit(X_train)
    return model

def predict(model, X_test):
    preds = model.predict(X_test)

    # 1 -> anomaly
    # 0 -> normal
    predicted = []
    for p in preds:
        if p == -1:
            predicted.append(1)
        else:
            predicted.append(0)
        
    return predicted
