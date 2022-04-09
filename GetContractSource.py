from etherscan.contracts import Contract
from etherscan.accounts import Account
import argparse

import json
import datetime
from pathlib import Path



defaultContractAddress = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"    # BAYCcontractAddress
 
output_root = "output"

# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('address', default = defaultContractAddress, type=str, nargs='*')


# Parse the argument
args = parser.parse_args()

address = args.address
print(f'address: {address}')


with open('./api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['EtherscanKey']

def writeFile(filePath, content):
    filePath.parent.mkdir(exist_ok=True, parents=True); 
    filePath.write_text(content, encoding="utf-8")
    return

# Get Contract
api = Contract(address=address, api_key=key)
contractContent = api.get_sourcecode()
contractSourceCode = contractContent[0]['SourceCode']
contractName = contractContent[0]['ContractName']
compilerVersion = contractContent[0]['CompilerVersion']

print(f"ContractName: {contractName}")
print(f"CompilerVersion: {compilerVersion}")


# 將合約 Source Code 寫入 output 目錄, 第一層為合約名稱, 第二層為 Source Code
if len(contractName):
    constractSourceCode = contractSourceCode.replace('\r\n', '\n')
    # 有多個合約 source
    if (constractSourceCode[:2] == "{{"):
        constractSourceCode = constractSourceCode[1:]
        constractSourceCode = constractSourceCode[:-1]

        data = json.loads(constractSourceCode)
        
        for attribute, value in data['sources'].items():
            curPath = Path(__file__).parent
            solFile = str(attribute)
            if solFile[:1] == "/":
                solFile = solFile[1:]
            print(solFile)
            output_file = Path(curPath, output_root, contractName, solFile); 
            writeFile(output_file, value['content'])

    else:  # 只有一個合約
        
        curPath = Path(__file__).parent
        solFile = str(contractName + ".sol")

        output_file = Path(curPath, output_root, contractName, solFile); 
        writeFile(output_file, constractSourceCode)



# 寫入 abi
abiContent = contractContent[0]['ABI']
curPath = Path(__file__).parent
abiFile = str(contractName + ".abi")
output_file = Path(curPath, output_root, contractName, abiFile); 
output_file.parent.mkdir(exist_ok=True, parents=True); 
output_file.write_text(abiContent, encoding="utf-8")


api = Account(address=address, api_key=key)

# Get First Block
tx = api.get_transaction_page(page=1, offset=1, sort='asc')
if len(tx)>0:
    firstResult = tx[0]
    print(f"First Block: blockNumber: {firstResult['blockNumber']}, timeStamp: {firstResult['timeStamp']}")
    
    timestamp = int(firstResult['timeStamp'])

    # # local time
    # value = datetime.datetime.fromtimestamp(timestamp)
    # print(f"{value:%Y-%m-%d %H:%M:%S}")

    # utc time
    value = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    print(f"utc time: {value:%Y-%m-%d %H:%M:%S}")

# Get Last Block
tx = api.get_transaction_page(page=1, offset=1, sort='desc')
if len(tx)>0:
    firstResult = tx[0]
    print(f"Last Block: blockNumber: {firstResult['blockNumber']}, timeStamp: {firstResult['timeStamp']}")
    timestamp = int(firstResult['timeStamp'])
    # utc time
    value = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    print(f"utc time: {value:%Y-%m-%d %H:%M:%S}")

