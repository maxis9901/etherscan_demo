from fileinput import filename
import pathlib
from etherscan.contracts import Contract
from etherscan.accounts import Account
from etherscan.logs import Logs
from web3 import Web3
import argparse
import pandas as pd
import json
import datetime
import os




defaultContractAddress = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"    # BAYCcontractAddress
output_root = "output"



# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('address', default = defaultContractAddress, type=str, nargs='*')

# Parse the argument
args = parser.parse_args()

address = args.address[0]
print(f'address: {address}')


with open('./api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['EtherscanKey']

def writeFile(filePath, content):
    filePath.parent.mkdir(exist_ok=True, parents=True); 
    filePath.write_text(content, encoding="utf-8")
    return


api = Account(address=address, api_key=key)

transactions = api.get_transaction_page(page=1, offset=10000, sort='asc')

# 另一種作法,但超過 1萬筆會有 error
# transactions = api.get_all_transactions(offset=10000, sort='asc', internal=False)

print(f'Total records: {len(transactions)}')                                        


data_df = pd.DataFrame(data=transactions)

# input 欄位內容太多,先取消
data_df = data_df.drop(columns = ["input"])

fileName = f'GetTransactions_{address}.csv' 
data_df.to_csv(os.path.join('./', output_root, fileName),index=False)
print("Process End")



'''
event_hash = Web3.keccak(text="Transfer(address,address,uint256)").hex()

api = Logs(api_key=API_KEY)
# 只會回傳前 1000 筆
result = api.get_logs(from_block= "12287507", topic0=event_hash)
print(len(result))
'''


