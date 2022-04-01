import web3
import  arrow
from hexbytes import HexBytes
import json
import arrow
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('t', default = ['2022/03/28','00:00:10'], type=str, nargs='*')
# parser.add_argument('t', default = ['1648080010'], type=str, nargs='*')


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

T = lambda i_block: web3.eth.getBlock(i_block).timestamp

ilatest = web3.eth.get_block('latest')['number']

def iblock_near(tunix_s, ipre=1, ipost=ilatest):
    ipre = max(1, ipre)
    ipost = min(ilatest, ipost)

    if ipre == ipost:
        # print('Got it')
        return ipre

    t0, t1 = T(ipre), T(ipost)

    av_block_time = (t1 - t0) / (ipost-ipre)

    # if block-times were evenly-spaced, get expected block number
    k = (tunix_s - t0) / (t1-t0)
    iexpected = int(ipre + k * (ipost - ipre))

    # get the ACTUAL time for that block
    texpected = T(iexpected)

    # use the discrepancy to improve our guess
    est_nblocks_from_expected_to_target = int((tunix_s - texpected) / av_block_time)
    iexpected_adj = iexpected + est_nblocks_from_expected_to_target

    # print()
    # print(f'target timestamp ({tunix_s}) lies {k:.3f} of the way from block# {ipre} (t={t0}) to block# {ipost} (t={t1})')
    # print(f'Expected block# assuming linearity: {iexpected} (t={texpected})')
    # print('Expected nblocks required to reach target (again assuming linearity):', est_nblocks_from_expected_to_target)
    # print('New guess at block #:', iexpected_adj)

    r = abs(est_nblocks_from_expected_to_target)

    return iblock_near(tunix_s, iexpected_adj - r, iexpected_adj + r)

startBlock = iblock_near(inputTime.timestamp())
print(f'near block: {startBlock}')

