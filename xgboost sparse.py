import pandas as pd
from sklearn.metrics import roc_auc_score
from scipy import sparse
import xgboost as xgb
import numpy as np

# Function to load the data in chunks and convert it to a sparse matrix
def load_data_in_chunks(file_path, chunk_size=10**6):
    chunk_list = []
    y_list = []
    for chunk in pd.read_csv(file_path, sep=",", chunksize=chunk_size):
        # Separate features and labels
        X_chunk = chunk.drop(columns=["Label"])
        y_chunk = chunk["Label"]
        
        # Convert boolean columns to integers (True -> 1, False -> 0)
        X_chunk = X_chunk.astype(int, errors='ignore')

        # Ensure all data is numeric
        X_chunk = X_chunk.apply(pd.to_numeric, errors='coerce')
        
        # Handle missing values by filling with zero
        X_chunk = X_chunk.fillna(0)
        
        # Convert to sparse format
        X_sparse_chunk = sparse.csr_matrix(X_chunk.values)
        chunk_list.append(X_sparse_chunk)
        y_list.append(y_chunk)
    
    # Combine chunks into one sparse matrix
    X_sparse = sparse.vstack(chunk_list)
    y_train = pd.concat(y_list, axis=0)
    return X_sparse, y_train

# Load training data in chunks
print("train")
X_train, y_train = load_data_in_chunks("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/one-hot/freq.csv")

# Load validation data
print("val")
val = pd.read_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Trainers/one-hot/val.csv")
x_val = val.drop(columns=["Label"])
y_val = val["Label"]

# Convert boolean columns to integers for validation data
x_val = x_val.astype(int, errors='ignore')

# Ensure validation data is numeric and handle missing values
x_val = x_val.apply(pd.to_numeric, errors='coerce')
x_val = x_val.fillna(0)
x_val_sparse = sparse.csr_matrix(x_val.values)

# Load test data
print("test")
test = pd.read_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Data TEST/one-hot/test filtrado oh.csv")
x_test = test.drop(columns=["id"])

# Convert boolean columns to integers for test data
x_test = x_test.astype(int, errors='ignore')

# Ensure test data is numeric and handle missing values
x_test = x_test.apply(pd.to_numeric, errors='coerce')
x_test = x_test.fillna(0)
x_test_sparse = sparse.csr_matrix(x_test.values)

# Train XGBoost model using DMatrix with sparse data
print("entrenamiento")
xgb_params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'colsample_bytree': 0.75,
    'gamma': 0.5,
    'learning_rate': 0.1,
    'max_depth': 8,
    'min_child_weight': 1,
    'n_estimators': 400,
    'reg_lambda': 0.5,
    'subsample': 0.75,
    'tree_method': 'hist'  # Use histogram-based tree method for large datasets
}

# Convert training and validation sets to DMatrix
dtrain = xgb.DMatrix(X_train, label=y_train)
dval = xgb.DMatrix(x_val_sparse, label=y_val)

# Train the model
clf_xgb = xgb.train(
    xgb_params,
    dtrain,
    num_boost_round=400,
    evals=[(dtrain, 'train'), (dval, 'val')],
    early_stopping_rounds=10
)

# Predict on test set
dtest = xgb.DMatrix(x_test_sparse)
preds_test_xgb = clf_xgb.predict(dtest)

# Save the predictions
avg_pred_df = pd.DataFrame({
    "id": test["id"],  # Correct access to the "id" column
    "pred": preds_test_xgb  # Predictions
})

# Save predictions to CSV
avg_pred_df.to_csv("C:/Users/estan/OneDrive/Escritorio/Cositas/facultad/TD VI/TP 2 - EL BOSQUE/DATA/Predicciones/oh_freq_xgb.csv", index=False)
