import requests
import time
import datetime
from interact import write_log
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

SLEEP_INTERVAL = 60 * 60  # 1 hora (en segundos)
TOKEN = 'TU_BOT_TOKEN'  # Reemplaza con tu token de Telegram
CHAT_ID = 'TU_CHAT_ID'  # Reemplaza con tu chat ID (el obtenido)

# Conexión con la red Ethereum
web3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))

if not web3.is_connected():
    print("❌ No se pudo conectar a la red")
    exit()

print("✅ Agente iniciado - monitoreando oportunidades cada hora")

# Función para enviar mensajes a Telegram
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

# Función para enviar notificación de inversión
def send_investment_notification(opportunity):
    message = f"🚀 Nueva Oportunidad de Inversión: {opportunity['symbol']} @ {opportunity['project']}\n"
    message += f"💰 APY: {opportunity['apy']:.2f}%\n"
    message += f"📊 TVL: ${opportunity['tvlUsd']:,}\n"
    message += f"🔗 [Haz clic aquí para más detalles](link_a_detalles)"  # Asegúrate de poner el enlace adecuado
    send_telegram_message(message)

# Simulación de cómo encontrar y notificar oportunidades
while True:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🕒 [{now}] Escaneando...")

    # Simulación de la nueva oportunidad (este dato vendría del código de ranking)
    new_opportunity = {
        'symbol': 'WETH-SNX',
        'project': 'Uniswap-V3',
        'apy': 64.09,
        'tvlUsd': 537175
    }

    # Enviar notificación de la nueva oportunidad
    send_investment_notification(new_opportunity)

    print(f"⏳ Esperando {SLEEP_INTERVAL // 60} minutos para la próxima ejecución...\n")
    time.sleep(SLEEP_INTERVAL)
