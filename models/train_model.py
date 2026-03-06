import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# Simulated training data
data = np.random.normal(size=(1000, 4))

model = IsolationForest(contamination=0.05)
model.fit(data)

joblib.dump(model, "models/isolation_model.pkl")
print("Model trained & saved.")