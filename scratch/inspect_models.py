import joblib
import os
import pandas as pd
import numpy as np

model_files = [
    'ml/model_xgb_baseline.pkl',
    'ml/model_xgb_smote.pkl',
    'ml/model_cat_baseline.pkl',
    'ml/model_cat_smote.pkl'
]

for file in model_files:
    print(f"\n{'='*50}")
    print(f"Inspecting: {file}")
    print(f"{'='*50}")
    
    try:
        model = joblib.load(file)
        
        # Check type
        print(f"Model type: {type(model)}")
        
        # Check features for XGBoost
        if hasattr(model, 'feature_names_in_'):
            print(f"Features (feature_names_in_): {model.feature_names_in_}")
        elif hasattr(model, 'get_booster'):
            # XGBoost booster
            booster = model.get_booster()
            print(f"Features (feature_names): {booster.feature_names}")
            
        # Check features for CatBoost
        if 'CatBoost' in str(type(model)):
            print(f"Features (feature_names_): {model.feature_names_}")
            
        # Try to get classes
        if hasattr(model, 'classes_'):
            print(f"Classes: {model.classes_}")
            
    except Exception as e:
        print(f"Error inspecting {file}: {e}")
