import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar los datos
data = pd.read_csv('investment_data.csv')

# Preprocesamiento de los datos
X = data[['APY', 'TVL']]  # Características de entrada (APY y TVL)
y = data['InvestmentScore']  # Lo que queremos predecir (Inversión Score)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el modelo
model = LinearRegression()

# Entrenar el modelo
model.fit(X_train, y_train)

# Predecir sobre los datos de prueba
y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Guardar el modelo entrenado (opcional)
import joblib
joblib.dump(model, 'investment_model.pkl')
