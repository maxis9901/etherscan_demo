import web3
import  arrow
from hexbytes import HexBytes
import json
import arrow
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
# parser.add_argument('t', default = ['2022/03/01','15:00:01'], type=str, nargs='*')
parser.add_argument('t', default = ['1648080010'], type=str, nargs='*')


# Parse the argument
args = parser.parse_args()

timeArg = ' '.join(args.t)

if len(args.t) == 1:
    inputTime = arrow.get(int(timeArg))
else:    
    inputTime = arrow.get(timeArg)

print(f'input time: {inputTime.format()} , timestamp: {inputTime.int_timestamp}')


with open('./api_key.json', mode='r') as key_file:
    infura_url = json.loads(key_file.read())['InfuraUrl']

# add your blockchain connection information
web3 = web3.Web3(web3.HTTPProvider(infura_url))
# get latest blocks
lastBlock = web3.eth.blockNumber

# 取得單一 Block
test =  web3.eth.getBlock(lastBlock)
# 取得第一筆資料的 TxHash
txHash =  HexBytes(test['transactions'][0]).hex()

# 取得這個 Block 中的 Tx count
txCount =  web3.eth.getBlockTransactionCount(lastBlock)



