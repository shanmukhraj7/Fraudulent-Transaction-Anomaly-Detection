import torch
import torch.nn as nn

class AutoEncoder(nn.Module):
    def __init__(self, input_data):
        super(AutoEncoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
        )

        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim),
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

    def train_autoencoder(X_train, epochs = 10, lr = 0.001):
        import torch.optim as opt
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        X_train_tensor = torch.tensor(X_train.values, dtype = torch.float32).to(device)

        model = AutoEncoder(input_dim = X_train.shape[1]).to(device)
        criterion = nn.MSELoss()
        optimizer = opt.Adam(model.parameters(), lr = lr)
        model.train()

        for epo in range(epochs):
            optimizer.zero_grad()
            outputs = model(X_train_tensor)
            loss = criterion(outputs, X_train_tensor)
            loss.backward()
            optimizer.step()

    def predict_autoencoder(model, X, threshold=None):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        X_tensor = torch.tensor(X.values, dtype=torch.float32).to(device)

        model.eval()
        with torch.no_grad():
            reconstructed = model(X_tensor)

        loss = torch.mean((X_tensor - reconstructed) ** 2, dim=1)
        loss = loss.cpu().numpy()

        if threshold is None:
            threshold = loss.mean() + 2 * loss.std()

        preds = []
        for l in loss:
            if l > threshold:
                preds.append(1)
            else:
                preds.append(0)

        return preds