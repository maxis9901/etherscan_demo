from web3 import Web3
import json
import requests

# Ref: https://medium.com/coinmonks/discovering-the-secrets-of-an-ethereum-transaction-64febb00935c


with open('./api_key.json', mode='r') as key_file:
    infura_url = json.loads(key_file.read())['InfuraUrl']

with open('./api_key.json', mode='r') as key_file:
    ETHERSCAN_API_KEY = json.loads(key_file.read())['EtherscanKey']

tx_hash = "0xac80bab0940f061e184b0dda380d994e6fc14ab5d0c6f689035631c81bfe220b"

web3 = Web3(
    Web3.HTTPProvider(
        infura_url,
        request_kwargs={"timeout": 60},
    )
)

# test
tx = web3.eth.get_transaction("0x22199329b0aa1aa68902a78e3b32ca327c872fab166c7a2838273de6ad383eba")
print(tx)



# Get transaction object
tx = web3.eth.get_transaction(tx_hash)
print(tx)





# Get ABI for smart contract NOTE: Use "to" address as smart contract 'interacted with'
abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={tx['to']}&apikey={ETHERSCAN_API_KEY}"
abi = json.loads(requests.get(abi_endpoint).text)
print(abi)

# Create Web3 contract object
contract = web3.eth.contract(address=tx["to"], abi=abi["result"])

# Decode input data using Contract object's decode_function_input() method
func_obj, func_params = contract.decode_function_input(tx["input"])
print(func_obj)

#    Transaction Log 

# Get transaction receipt
receipt = web3.eth.get_transaction_receipt(tx_hash)

# Isolate log to decode
log = receipt["logs"][0]
# Get smart contract address where log was initiated
smart_contract = log["address"]


# Get ABI of contract
abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={smart_contract}&apikey={ETHERSCAN_API_KEY}"
abi = json.loads(requests.get(abi_endpoint).text)


# Create contract object
contract = web3.eth.contract(smart_contract, abi=abi["result"])

# Get event signature of log (first item in topics array)
receipt_event_signature_hex = web3.toHex(log["topics"][0])


# Find ABI events
abi_events = [abi for abi in contract.abi if abi["type"] == "event"]

# Determine which event in ABI matches the transaction log you are decoding
for event in abi_events:
    # Get event signature components
    name = event["name"]
    inputs = [param["type"] for param in event["inputs"]]
    inputs = ",".join(inputs)
    # Hash event signature
    event_signature_text = f"{name}({inputs})"
    event_signature_hex = web3.toHex(web3.keccak(text=event_signature_text))
    # Find match between log's event signature and ABI's event signature
    if event_signature_hex == receipt_event_signature_hex:
        # Decode matching log
        # 回傳1至多筆同樣名稱的  event log
        decoded_logs = contract.events[event["name"]]().processReceipt(receipt)
        print(decoded_logs)

