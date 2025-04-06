from web3 import Web3
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

INFURA_URL = os.getenv("https://optimism-sepolia.infura.io/v3/8af29e1898c3498db06e4463c3f5c746")
PRIVATE_KEY = os.getenv("06e9cce03f794e6d52baa4afedc7f02e60d20e066731d5afe9af64ad9fa97fdf")
PUBLIC_ADDRESS = os.getenv("0x05b46a25D7363Cb2DEc7dB42b4E4e994BA59007e")

# Conexión a la blockchain
web3 = Web3(Web3.HTTPProvider("https://optimism-sepolia.infura.io/v3/8af29e1898c3498db06e4463c3f5c746"))

if web3.is_connected():
    print("✅ Conectado a Optimism correctamente.")
    print(f"📍 Dirección conectada: {0x05b46a25D7363Cb2DEc7dB42b4E4e994BA59007e}")
else:
    print("❌ No se pudo conectar a la red.")