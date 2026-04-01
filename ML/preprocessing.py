import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_dataset(path):
    df = pd.read_csv(path)
    return df

def preprocessing_data(df):
    df = df.copy()
    X = df.drop("Class", axis = 1)
    y = df["Class"]

    scaler = StandardScaler()
    X["Amount"] = scaler.fit_transform(X[["Amount"]])
    X["Time"] = scaler.fit_transform(X[["Time"]])

    return X, y
    