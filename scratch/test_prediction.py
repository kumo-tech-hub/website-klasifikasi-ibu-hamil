import joblib
import pandas as pd
import numpy as np

model_files = [
    'ml/model_xgb_baseline.pkl',
    'ml/model_xgb_smote.pkl',
    'ml/model_cat_baseline.pkl',
    'ml/model_cat_smote.pkl'
]

# Input data from screenshot
data = [[28, 50.0, 159.0, 19.78, 24.0]]
cols = ['umur', 'berat_badan_awal', 'tinggi', 'imt_sebelum_hamil', 'lila']
input_df = pd.DataFrame(data, columns=cols)

mapping = {0: 'Kurang', 1: 'Normal', 2: 'Lebih', 3: 'Obesitas'}

for file in model_files:
    print(f"\nModel: {file}")
    try:
        model = joblib.load(file)
        
        # Predict
        pred = model.predict(input_df.values)[0]
        
        # Probability
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(input_df.values)[0]
            print(f"Prediction: {pred} ({mapping.get(pred, 'Unknown')})")
            for i, p in enumerate(proba):
                print(f"  {mapping[i]}: {p*100:.2f}%")
        else:
            print(f"Prediction: {pred} ({mapping.get(pred, 'Unknown')})")
            
    except Exception as e:
        print(f"Error: {e}")
