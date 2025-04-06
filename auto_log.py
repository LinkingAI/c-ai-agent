import json
import os
from dotenv import load_dotenv
from web3 import Web3
from rank_opportunities import ranked  # Asegúrate que `rank_opportunities.py` tenga `ranked` exportado
import datetime

# 🔐 Cargar variables de entorno
load_dotenv()
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

# 🔗 Conexión con Web3
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    print("❌ No se pudo conectar a Sepolia")
    exit()
print("✅ Conectado a Sepolia")

# 📦 Cargar ABI
with open('./abi/AIInvestmentLog.json', 'r') as f:
    contract_abi = json.load(f)['abi']

# 📍 Dirección del contrato desplegado
CONTRACT_ADDRESS = "0xcD46f4efa24825B64de5f52f3493496B6a2Ae51B"
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# 🧠 Escoger la mejor oportunidad
top_op = ranked[0]  # la mejor del ranking
tokens = top_op['symbol']
protocol = top_op['project']
apy = top_op['apy']

# 📝 Formar el mensaje
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
message = f"Inversión en {tokens} @ {top_op['project']} con APY del {top_op['apy']:.2f}%"
print(f"📝 Mensaje generado: {message}")

# ✍️ Firmar y enviar transacción
def write_log_auto(msg):
    nonce = web3.eth.get_transaction_count(PUBLIC_ADDRESS)
    tx = contract.functions.logInvestment(msg).build_transaction({
        'from': PUBLIC_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': web3.to_wei('0.1', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"✅ Transacción enviada: {web3.to_hex(tx_hash)}")

write_log_auto(message)

import joblib

# Cargar el modelo
model = joblib.load('investment_model.pkl')

# Nueva oportunidad de inversión (esto puede ser parte de tu flujo de trabajo)
new_opportunity = [[65.00, 600000]]  # Ejemplo de APY y TVL

# Predecir el "score" de la inversión
predicted_score = model.predict(new_opportunity)

# Mostrar el puntaje predicho
print(f"Predicted Investment Score: {predicted_score[0]}")

# Tomar una decisión de inversión basada en el puntaje
if predicted_score[0] > 0.8:
    print("¡Inversión recomendada!")
else:
    print("Inversión no recomendada.")
