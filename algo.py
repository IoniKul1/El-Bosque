import pandas as pd
import numpy as np
import xgboost as xgb
import time
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, make_scorer
from sklearn.model_selection import ParameterSampler
from sklearn.metrics import confusion_matrix

random_state = 42
np.random.seed(random_state)

data = pd.read_csv('ctr_15.csv', sep = ',')
print(data.head())

#One hot encoding

df_features = data.drop(columns=['Label'])

df_ohe = pd.get_dummies(
    df_features,
    columns=[
        'action_categorical_0', 'action_categorical_1', 'action_categorical_2', 'action_categorical_3', 
        'action_categorical_4', 'action_categorical_5', 'action_categorical_6', 'action_categorical_7', 
        'action_list_0', 'action_list_1', 'action_list_2', 'auction_boolean_0', 'auction_boolean_1', 
        'auction_boolean_2', 'auction_categorical_0', 'auction_categorical_1', 'auction_categorical_2', 
        'auction_categorical_3', 'auction_categorical_4', 'auction_categorical_5', 'auction_categorical_6', 
        'auction_categorical_7', 'auction_categorical_8', 'auction_categorical_9', 'auction_categorical_10', 
        'auction_categorical_11', 'auction_categorical_12', 'auction_list_0', 'creative_categorical_0', 
        'creative_categorical_1', 'creative_categorical_10', 'creative_categorical_11', 
        'creative_categorical_12', 'creative_categorical_2', 'creative_categorical_3', 'creative_categorical_4', 
        'creative_categorical_5', 'creative_categorical_6', 'creative_categorical_7', 'creative_categorical_8', 
        'creative_categorical_9', 'device_id_type', 'gender'
    ],
    dummy_na=False,
    dtype=int
)
print(df_ohe.info())
print(df_ohe.head())




X = data.drop('Label', axis=1)
y = data['Label']

X_train, X_tmp, y_train, y_tmp = train_test_split(X, y,
                                                  train_size=0.7,
                                                  random_state=random_state,
                                                  stratify=y)

X_val, X_test, y_val, y_test = train_test_split(X_tmp, y_tmp,
                                                train_size=0.5,
                                                random_state=random_state,
                                                stratify=y_tmp)

print(f'Cantidad de datos de entrenamiento: {len(X_train)}')
print(f'Cantidad de datos de validación: {len(X_val)}')
print(f'Cantidad de datos de prueba: {len(X_test)}')

#clf_xgb = xgb.XGBClassifier(objective = 'binary:logistic',
                           # seed = random_state,
                           # eval_metric = 'auc')

#clf_xgb.fit(X_train, y_train, verbose = True, eval_set = [(X_val, y_val)])