# etherscan api demo
使用 [py-etherscan-api](https://github.com/corpetty/py-etherscan-api) 呼叫 etherscan api 查詢 Blockchain 的資料,並將結果存成 csv 檔放在 output 目錄

使用時需先到 Etherscan 註冊帳號，並將 key 填入 api_key.json

有些範例用 [Web3.py](https://github.com/ethereum/web3.py)，使用時需先到 [infura](https://infura.io/) 註冊，並將 key 填入 api_key.json



## GetBlockTransaction: 取得區塊內的 Transaction
---
參數：傳入2個參數，分別為開始及結束的 block no

csv 檔案多了 contractName, contractAddress 欄位，目的在取得 transaction 時會檢查 to 欄位是否為合約地址，為合約地址會再抓合約的名稱，將合約名稱及地址放在 contractName, contractAddress 欄位

下例取得 block 12292922 到 12292930 的資料
```
python GetBlockTransaction.py 12292922 12292930
```

## GetContractSource: 取得合約 source code 及 ABI
---
若已經知道合約地址，可以用 GetContractSource 下載合約程式碼跟 ABI，支援合約有多個檔案的情況，下載時會在 output 目錄下產生合約名稱的目錄，再將 source code 放到此目錄

參數:合約地址

下例取得無聊猿 NFT 合約程式，合約的名稱為 BoredApeYachtClub，所以 output 目錄下會產生BoredApeYachtClub 目錄，再把下載的合約程式及 ABI 放到此目錄
```
python GetContractSource.py 0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
```

## GetTransactions: 取得某地址的Transaction
---
依地址查詢所有的 Transaction，Etherscan API 有限制每次最多只能抓１萬筆，若筆數超過時只會回傳前１萬筆資料

參數：合約地址
```
python GetTransactions.py 0x7169887b559F625a81144eeE8AC784d1D8B4920F
```

## GetBlockByTimestamp: 輸入時間,取得最接近此時間的 BlockNo
---
依時間取得此時間之前最後一筆的 block no，目前程式有 bug，有時候會抓到倒數第二筆 block，這部份還在查原因

參數：日期時間，可以輸入 年/月/日 時:分:秒 的格式，或是輸入 unix time
```
# 使用 年/月/日 時:分:秒 的格式
python GetBlockByTimestamp.py 2022/3/28 00:00:10

# unix time
python GetBlockByTimestamp.py 1648080010

```

## GetLogs: 取得 Logs
---
取得 Logs，現在只實作取得 Transfer 的 Log , 若要取得其它的 Log 可自行調整，因為 Etherscan API 的限制只能取得 1000 筆資料

參數:合約地址及 block 起迄號碼
```
python GetLogs.py --address 0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D --block 12287507 14467905
```