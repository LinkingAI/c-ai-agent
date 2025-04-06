import os
import requests
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Obtener las variables de entorno
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Verificar si las variables están cargadas
if not TOKEN or not CHAT_ID:
    print("❌ Error: El token o el chat ID no están configurados correctamente.")
else:
    print("✅ Variables de entorno cargadas correctamente.")

# Mensaje de prueba
message = "¡Este es un mensaje de prueba!"

# URL para la API de Telegram
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Parámetros para enviar el mensaje
payload = {
    'chat_id': CHAT_ID,
    'text': message
}

# Intentar enviar el mensaje
try:
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Mensaje enviado correctamente.")
    else:
        print(f"❌ Error al enviar el mensaje: {response.status_code} - {response.text}")
except Exception as e:
    print(f"⚠️ Error al intentar enviar el mensaje: {e}")
