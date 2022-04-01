from etherscan.blocks import Blocks
from etherscan.contracts import Contract
from etherscan.accounts import Account
from etherscan.proxies import Proxies
from web3 import Web3

import json
import datetime
from pathlib import Path
import pandas as pd
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('block', default = [12287507,12287507], type=int, nargs='*')  # default is BAYC contract block

# Parse the argument
args = parser.parse_args()

startBlock = args.block[0]
endBlock = args.block[1]
print(f'Block {startBlock} to {endBlock}')



dataList = list()



def copyTran(dataList, tran) -> dict:
    dataDic = dict()
    dataDic["blockHash"] = tran["blockHash"]
    dataDic["blockNumber"] = int(tran["blockNumber"], 16)
    dataDic["from"] = tran["from"]
    dataDic["gas"] = tran["gas"]
    dataDic["gasPrice"] = tran["gasPrice"]
    dataDic["hash"] = tran["hash"]

    # 內容太多,先取消
    # dataDic["input"] = tran["input"]
    
    dataDic["nonce"] = tran["nonce"]
    dataDic["to"] = tran["to"]

    dataDic["contractName"] = ""
    dataDic["contractAddress"] = ""
    
    dataList.append(dataDic)
    return dataDic



with open('./api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['EtherscanKey']

# 取得 BlockNo 中所有 Transactions
proxyApi = Proxies(api_key=key)

currentBlock = startBlock
while currentBlock <= endBlock:
    block = proxyApi.get_block_by_number(currentBlock)
    # print(block['transactions'])
    contractMap = dict()
    # 列出所有的 Transaction
    for tran in block['transactions']:
        # print(tran)
        tranDic = copyTran(dataList, tran)
        toAddress = tranDic["to"]
        if toAddress == None:
            continue

        if toAddress in contractMap.keys():
            continue
        
        contractMap[toAddress] = toAddress
        contractApi = Contract(address=toAddress, api_key=key)
        contractContent = contractApi.get_sourcecode()
        contractName = contractContent[0]['ContractName']
        # update address -> contract name
        contractMap[toAddress] = contractName
        tranDic["contractName"] = contractName
        tranDic["contractAddress"] = toAddress
        if len(contractName):
            print(f"find contract, {contractName}")

        
    currentBlock += 1

data_df = pd.DataFrame(data=dataList)
data_df.to_csv('./output/GetBlockTransaction.csv',index=False)
print("Process End")