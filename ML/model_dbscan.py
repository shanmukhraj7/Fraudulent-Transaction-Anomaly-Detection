from sklearn.cluster import DBSCAN

def train_dbscan(X_train):
    model = DBSCAN(
        eps = 3, 
        min_samples = 10
    )
    preds = model.fit_predict(X_train)
    return preds