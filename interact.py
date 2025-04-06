import os
from dotenv import load_dotenv
from web3 import Web3

# ✅ Cargar variables del .env
load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

# ✅ Dirección del contrato ya desplegado
CONTRACT_ADDRESS = "0xcD46f4efa24825B64de5f52f3493496B6a2Ae51B"

# ✅ ABI del contrato (puedes copiarlo también desde el archivo JSON si quieres)
ABI = [
    {
        "inputs": [{"internalType": "string", "name": "_message", "type": "string"}],
        "name": "logInvestment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "getLog",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalLogs",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ✅ Conexión a Infura
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not web3.is_connected():
    print("❌ No se pudo conectar a la red")
    exit()

print("✅ Conectado a Sepolia")

# ✅ Configurar contrato
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# ✅ Crear función para escribir un log
def write_log(message):
    nonce = web3.eth.get_transaction_count(PUBLIC_ADDRESS)

    tx = contract.functions.logInvestment(message).build_transaction({
        'from': PUBLIC_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': web3.to_wei('0.1', 'gwei')
    })

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"✅ Transacción enviada: {web3.to_hex(tx_hash)}")



# ✅ Leer logs previos
def read_logs():
    total = contract.functions.totalLogs().call()
    print(f"📚 Total de logs: {total}")
    for i in range(total):
        log = contract.functions.getLog(i).call()
        print(f"📝 Log #{i}: {log}")

# ✅ Prueba
if __name__ == "__main__":
    print("👉 Opciones: ")
    print("1. Registrar decisión")
    print("2. Ver historial")
    choice = input("¿Qué quieres hacer? ")

    if choice == "1":
        msg = input("Escribe el mensaje a registrar: ")
        write_log(msg)
    elif choice == "2":
        read_logs()
    else:
        print("❌ Opción no válida")
