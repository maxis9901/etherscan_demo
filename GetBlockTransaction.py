from etherscan.contracts import Contract
from etherscan.proxies import Proxies
import json
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

def getNewContractAddress(txNo):
    '''
    取得 Transcation 的 contractAddress 內容
    '''
    api = Proxies(api_key=key)
    receipt = api.get_transaction_receipt(tx_hash = txNo)
    return receipt['contractAddress']

def checkIsContractAddress(address):
    '''
    判斷是否為合約地址
    '''
    proxyApi = Proxies(api_key=key)
    receipt = proxyApi.get_code(address = address)
    # 判斷是否為合約, 合約回傳 byteCode, 不是合約回傳 0x
    return receipt != '0x'


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
        contractName = ""
        contractAddress = ""
        isContractAddress = False
        if toAddress == None:
            contractAddress =  getNewContractAddress(tran['hash'])
            isContractAddress = True
        else:
            # 判斷是否為合約地址
            isContractAddress = checkIsContractAddress(toAddress)
            if isContractAddress:
                contractAddress =  toAddress


        if contractAddress in contractMap.keys():
            continue
        
        # 為合約地址
        if isContractAddress:
            contractMap[contractAddress] = contractAddress
            contractApi = Contract(address=contractAddress, api_key=key)
            contractContent = contractApi.get_sourcecode()
            contractName = contractContent[0]['ContractName']
            # update address -> contract name
            contractMap[contractAddress] = contractName


        tranDic["contractName"] = contractName
        tranDic["contractAddress"] = contractAddress

        if len(contractName):
            print(f"find contract, {contractName}")

        
    currentBlock += 1

data_df = pd.DataFrame(data=dataList)
data_df.to_csv('./output/GetBlockTransaction.csv',index=False)
print("Process End")