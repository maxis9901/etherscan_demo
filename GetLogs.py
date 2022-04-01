from etherscan.contracts import Contract
from etherscan.accounts import Account
from etherscan.logs import Logs
from web3 import Web3
import argparse
import json
import datetime
from pathlib import Path
import pandas as pd
import os

defaultContractAddress = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"    # BAYCcontractAddress
output_root = "output"

# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('--address', default = defaultContractAddress, type=str)
parser.add_argument('--block', default = [12287507,14467905], type=int, nargs='*')  # default is BAYC contract block


# Parse the argument
args = parser.parse_args()

address = args.address
startBlock = args.block[0]
endBlock = args.block[1]

print(f'address: {address}')


with open('./api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['EtherscanKey']



event_hash = Web3.keccak(text="Transfer(address,address,uint256)").hex()

api = Logs(api_key=key)

api.url_dict[api.ADDRESS] = address

# 只會回傳前 1000 筆
log = api.get_logs(from_block= startBlock, to_block = endBlock, topic0=event_hash)
print('Total logs:', len(log))



data_df = pd.DataFrame(data=log)


fileName = f'GetLogs.csv' 
data_df.to_csv(os.path.join('./', output_root, fileName),index=False)
print("Process End")