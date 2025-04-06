import requests
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# 1. Configuración
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("SEPOLIA_RPC")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

ABI_PATH = "./abi/AIInvestmentLog.json"
with open(ABI_PATH, "r") as f:
    contract_abi = f.read()

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# 2. Obtener oportunidades de DefiLlama
def get_opportunities():
    url = "https://yields.llama.fi/pools"
    res = requests.get(url)
    data = res.json()

    optimism_pools = [p for p in data['data'] if p['chain'] == 'Optimism']
    ranked = sorted(
        optimism_pools,
        key=lambda x: float(x.get("apy", 0)) * float(x.get("tvlUsd", 0)),
        reverse=True
    )
    return ranked[:1]  # solo top 1

# 3. Registrar en blockchain
def log_investment(message):
    nonce = web3.eth.get_transaction_count(account.address)
    tx = contract.functions.logInvestment(message).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": web3.to_wei("1", "gwei"),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"✅ Decisión registrada en tx: {web3.to_hex(tx_hash)}")

# 4. Ejecutar lógica
def run_agent():
    print("🤖 Evaluando oportunidades...")
    top = get_opportunities()
    if not top:
        print("⚠️ No se encontraron oportunidades.")
        return

    opportunity = top[0]
    msg = f"Inversión en {opportunity['symbol']} @ {opportunity['project']} | APY: {opportunity['apy']}%"
    print("📌 Decisión:", msg)

    log_investment(msg)

# 👇 Ejecutar
if __name__ == "__main__":
    run_agent()
