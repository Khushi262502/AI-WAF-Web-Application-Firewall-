import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def extract_features(req):
     req = req.lower()
     return [
          len(req),
          req.count("'"),
          1 if "or 1=1" in req else 0,
          1 if "<script>" in req else 0,
        ]
data = pd.read_csv("data.csv")

X = data["request"].apply(extract_features).tolist()
y = data["label"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X,y)

joblib.dump(model, "waf_model.pkl")

print("Model trained successfully!")
