import joblib
import traceback

print("Trying to load models with joblib...")

cat_smote_path = "model_cat_smote.pkl"
xgb_smote_path = "model_xgb_smote.pkl"

try:
    cat_model = joblib.load(cat_smote_path)
    print(f"Successfully loaded {cat_smote_path}!")
except Exception as e:
    print(f"Error loading {cat_smote_path}:")
    traceback.print_exc()

try:
    xgb_model = joblib.load(xgb_smote_path)
    print(f"Successfully loaded {xgb_smote_path}!")
except Exception as e:
    print(f"Error loading {xgb_smote_path}:")
    traceback.print_exc()
