from web3 import Web3
from dotenv import load_dotenv
import os

# Cargar variables del .env
load_dotenv()

INFURA_URL = os.getenv("https://optimism-sepolia.infura.io/v3/8af29e1898c3498db06e4463c3f5c746")
PRIVATE_KEY = os.getenv("06e9cce03f794e6d52baa4afedc7f02e60d20e066731d5afe9af64ad9fa97fdf")
PUBLIC_ADDRESS = os.getenv("0x05b46a25D7363Cb2DEc7dB42b4E4e994BA59007e")

# Crear conexión Web3
web3 = Web3(Web3.HTTPProvider("https://optimism-sepolia.infura.io/v3/8af29e1898c3498db06e4463c3f5c746"))

if web3.is_connected():
    print("✅ Conectado a Optimism Sepolia")

    # Obtener nonce actual
    nonce = web3.eth.get_transaction_count("0x05b46a25D7363Cb2DEc7dB42b4E4e994BA59007e")

    # Armar una transacción de test: se envía a sí misma 0.0001 ETH
    tx = {
        'nonce': nonce,
        'to': PUBLIC_ADDRESS,
        'value': web3.to_wei(0.0001, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('0.01', 'gwei'),
        'chainId': 11155420  # Optimism Sepolia
    }

    # Firmar transacción con clave privada
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)


    # Mostrar transacción firmada
    print("\n🔐 Transacción firmada (no enviada):")
    print(web3.to_hex(signed_tx.rawTransaction))

    # Confirmar si deseas enviarla
    send = input("\n¿Quieres enviarla a la red? (s/n): ")
    if send.lower() == 's':
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"📤 Transacción enviada. Hash: {web3.to_hex(tx_hash)}")
        print("🌐 Puedes verla en: https://sepolia-optimism.etherscan.io/tx/" + web3.to_hex(tx_hash))
    else:
        print("⏹ Transacción firmada pero no enviada.")
else:
    print("❌ No se pudo conectar a Optimism Sepolia.")
