import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from mutation_engine import generate_mutations

def retrain_model(original_payload):
    data = pd.read_csv("data.csv")
    mutations = generate_mutations(original_payload)
    for attack in mutations:
         new_row = {"request": attack , "label":1}
         data = pd.concat([data, pd.DataFrame([new_row])], ignore_index = True)
    data.to_csv("data.csv",index=False)
    
    def extract_features(req):
        req = req.lower()
        return [
             len(req),
             req.count("'"),
             1 if "or 1=1" in req else 0,
             1 if "<script>" in req else 0
        ]
    X = data["request"].apply(extract_features).tolist()
    y = data["label"]
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X,y)
    
    joblib.dump(model , "waf_model.pkl")
    print("Model retrained with mutations!")
             
