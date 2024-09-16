import pandas as pd
import numpy as np
import xgboost as xgb

# Configuración de pandas para mostrar todas las columnas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Cargar los datos
data_reducido = pd.read_csv("/Users/ionikullock/Desktop/UTDT-Tecnología Digital/TD VI/Trabajo práctico 2/Datos/data_reducido.csv")
data_test = pd.read_csv("/Users/ionikullock/Desktop/UTDT-Tecnología Digital/TD VI/Trabajo práctico 2/Datos/ctr_test.csv")

# Eliminar columnas innecesarias
columns_to_remove = ['device_id', 'action_list_1', 'action_list_2', 'action_categorical_0', 
                     'auction_list_0', 'action_categorical_2', 'action_categorical_4', 'auction_categorical_0', 
                     'auction_categorical_11', 'auction_categorical_3', 'creative_categorical_0',
                     'auction_categorical_7', 'auction_age', 'auction_categorical_12', 'auction_categorical_9',
                     'creative_categorical_12', 'creative_categorical_2', 'creative_categorical_5', 
                     'creative_categorical_6', 'creative_categorical_7']
data_reducido = data_reducido.drop(columns=columns_to_remove, errors='ignore')
data_test = data_test.drop(columns=columns_to_remove, errors='ignore')

# Seleccionar y codificar las columnas categóricas
columns_to_encode = [
    'action_categorical_1', 'action_categorical_3',
    'auction_categorical_8', 'creative_categorical_11', 'creative_categorical_4', 'creative_categorical_8',
    'creative_categorical_9', 'device_id_type'
]

# Función para aplicar One-Hot Encoding
def apply_one_hot_encoding(df, columns):
    df_encoded = df.copy()
    for col in columns:
        if col in df_encoded.columns:
            df_encoded = pd.get_dummies(df_encoded, columns=[col], drop_first=False, dtype=int)
    return df_encoded

# Codificar las columnas en ambos conjuntos de datos
data_encoded = apply_one_hot_encoding(data_reducido, columns_to_encode)
data_encoded_test = apply_one_hot_encoding(data_test, columns_to_encode)

# Alinear las columnas entre el conjunto de entrenamiento y el de prueba
all_columns = sorted(set(data_encoded.drop(columns=['Label']).columns).union(set(data_encoded_test.columns)))

data_encoded = data_encoded.reindex(columns=all_columns, fill_value=0)
data_encoded_test = data_encoded_test.reindex(columns=all_columns, fill_value=0)

# Separar características y etiquetas del conjunto de entrenamiento
X_train = data_encoded.drop('Label', axis=1)
y_train = data_encoded['Label']

# Cargar el modelo entrenado
random_state = 42
clf_xgb = xgb.XGBClassifier(objective='binary:logistic', seed=random_state, eval_metric='auc')

# Si ya has entrenado el modelo, carga el modelo aquí (en lugar de ajustar)
# clf_xgb = xgb.XGBClassifier().load_model('path_to_model_file')  # O usar el modelo ya entrenado en el código

# Entrenar el modelo (comentar esta línea si ya has entrenado el modelo previamente)
clf_xgb.fit(X_train, y_train)

# Predecir en el conjunto de prueba
X_test = data_encoded_test.drop('id', axis=1, errors='ignore')  # Asegúrate de que 'id' no esté en X_test
y_test_pred_xgb = clf_xgb.predict_proba(X_test)[:, 1]  # Probabilidad de la clase positiva

# Crear el DataFrame de envío
submission_df = pd.DataFrame({
    'id': data_test['id'],  # Usa la columna 'id' del archivo data_test.csv
    'Label': y_test_pred_xgb  # Las predicciones del modelo
})

# Guardar el archivo CSV para el envío
submission_df.to_csv('submission_xgb.csv', index=False)

print("Archivo 'submission_xgb.csv' generado con éxito.")