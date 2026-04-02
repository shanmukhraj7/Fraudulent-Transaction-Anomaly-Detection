import pandas as pd
from sklearn.decomposition import PCA

def apply_pca(X, n_components=0.95):
    # Applying PCA to reduce dimensionality while preserving N important features
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X)
    
    columns = [f"PCA_{i+1}" for i in range(X_pca.shape[1])]
    return pd.DataFrame(X_pca, columns=columns, index=X.index), pca

def create_features(df):
    df_engineered = df.copy()
    
    # Converting Time into Hours
    if 'Time' in df_engineered.columns:
        df_engineered['Hour'] = (df_engineered['Time'] // 3600) % 24
        
    return df_engineered
