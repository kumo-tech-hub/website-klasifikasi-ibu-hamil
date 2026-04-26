import joblib
import pandas as pd
import numpy as np

model_files = [
    'ml/model_xgb_baseline.pkl',
    'ml/model_xgb_smote.pkl',
    'ml/model_cat_baseline.pkl',
    'ml/model_cat_smote.pkl'
]

# Scenario: BB Awal 50, BB Sekarang 53, Tinggi 148, LiLA 20, Umur 28
# IMT = 50 / (1.48^2) = 22.82
data = [[28, 50.0, 148.0, 22.82, 20.0]]
cols = ['umur', 'berat_badan_awal', 'tinggi', 'imt_sebelum_hamil', 'lila']
input_df = pd.DataFrame(data, columns=cols)

# mapping dari kode (0: Kurang, 1: Lebih, 2: Normal, 3: Obesitas)
# Sesuai perbaikan mapping terakhir: 0: Kurang, 1: Lebih, 2: Normal, 3: Obesitas
mapping = {0: 'Kurang', 1: 'Lebih', 2: 'Normal', 3: 'Obesitas'}

for file in model_files:
    print(f"\nModel: {file}")
    try:
        model = joblib.load(file)
        
        # Predict class
        pred = model.predict(input_df.values)[0]
        
        # Probability breakdown
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(input_df.values)[0]
            print(f"Prediction: {pred} ({mapping.get(pred, 'Unknown')})")
            
            # Find index of 'Kurang'
            # Assuming labels in model are [0, 1, 2, 3]
            for i, p in enumerate(proba):
                print(f"  - {mapping[i]}: {p*100:.2f}%")
                
            # Confidence is max proba
            confidence = max(proba) * 100
            print(f"Confidence (Keyakinan): {confidence:.2f}%")
            print(f"Probabilitas Kurang: {proba[0]*100:.2f}%")
    except Exception as e:
        print(f"Error: {e}")
