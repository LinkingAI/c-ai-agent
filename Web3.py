from web3 import Web3
import json

# Connect to the Ethereum network using Infura or your local node
infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Set the contract address and ABI
contract_address = "YOUR_CONTRACT_ADDRESS"
contract_abi = json.loads('[YOUR_ABI]')  # Replace with actual ABI from Remix

# Set up the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Listen to the InvestmentLogged event
event_filter = contract.events.InvestmentLogged.createFilter(fromBlock='latest')

# Function to fetch the logs
def get_investment_logs():
    logs = event_filter.get_new_entries()
    for log in logs:
        print(f"New investment: {log.args.investmentMessage}")
    
# Poll for new logs every 10 seconds
import time
while True:
    get_investment_logs()
    time.sleep(10)
