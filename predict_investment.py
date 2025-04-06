import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Función para cargar el modelo previamente entrenado
def load_model():
    return joblib.load('investment_model.pkl')

# Función para guardar el modelo actualizado
def save_model(model):
    joblib.dump(model, 'investment_model.pkl')

# Función para entrenar el modelo con nuevos datos
def train_model(new_data, labels):
    model = load_model()  # Cargar el modelo
    model.fit(new_data, labels)  # Reentrenar el modelo con nuevos datos
    save_model(model)  # Guardar el modelo actualizado
    return model  # Devolver el modelo actualizado

# Predicción para una nueva inversión
def predict_investment(new_opportunity):
    model = load_model()  # Cargar el modelo
    predicted_score = model.predict(new_opportunity)
    return predicted_score[0]

# Función principal
def main():
    # Simulación de nuevas oportunidades de inversión (APY y TVL)
    new_investments = np.array([[66.5, 700000], [62.5, 800000]])  # Nuevos APY y TVL
    investment_labels = np.array([1, 0])  # 1 = buena inversión, 0 = mala inversión

    # Reentrenar el modelo con los nuevos datos
    updated_model = train_model(new_investments, investment_labels)

    # Predicción con el modelo actualizado
    new_opportunity = [[65.00, 750000]]  # APY y TVL de una nueva oportunidad
    predicted_score = predict_investment(new_opportunity)
    print(f"Predicted Investment Score: {predicted_score}")

if __name__ == "__main__":
    main()
