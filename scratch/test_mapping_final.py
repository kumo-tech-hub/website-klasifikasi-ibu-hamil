import joblib
import pandas as pd
import numpy as np

model_files = [
    'ml/model_xgb_baseline.pkl'
]

# Case 1: Normal (from user screenshot)
data_normal = [[28, 50.0, 159.0, 19.78, 24.0]]
# Case 2: Lebih (from Row 18)
data_lebih = [[44, 69.0, 155.0, 28.72, 31.0]]
# Case 3: Obesitas (from Row 31)
data_obesitas = [[24, 80.0, 155.0, 33.3, 27.0]]

cols = ['umur', 'berat_badan_awal', 'tinggi', 'imt_sebelum_hamil', 'lila']

for file in model_files:
    print(f"\nModel: {file}")
    model = joblib.load(file)
    
    pred_normal = model.predict(pd.DataFrame(data_normal, columns=cols).values)[0]
    pred_lebih = model.predict(pd.DataFrame(data_lebih, columns=cols).values)[0]
    pred_obesitas = model.predict(pd.DataFrame(data_obesitas, columns=cols).values)[0]
    
    print(f"Normal input   -> Predicted class: {pred_normal}")
    print(f"Lebih input    -> Predicted class: {pred_lebih}")
    print(f"Obesitas input -> Predicted class: {pred_obesitas}")
