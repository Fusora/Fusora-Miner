import requests, json,  np, threading, hashlib, binascii, yaml
from datetime import datetime
from time import time
from Block import *
from Worker import *


def getJobs(address):
    jobs = requests.get('https://fusora.herokuapp.com/mining/get-mining-job/'+address)
    result = json.dumps(jobs.json())
    return yaml.safe_load(result)

def submitMinedBlock(block):
    # 6a8a742eaec8399a3fd48a91a227b9fdc003a484
    print(block)
    response = requests.post('https://fusora.herokuapp.com/mining/submit-mined-block', json=block)
    print(response.status_code)
    print(response.json())

def mine(blockData, nonce, address):
    # print(blockData)
    blockDataHash = blockData['blockDataHash']
    difficulty = blockData['difficulty']
    prevBlockHash = blockData['prevBlockHash']
    transactions = blockData['transactions']
    index = blockData['index']
    timestamp = time()/1000
    block = Block(blockDataHash, 
        difficulty,
        nonce, 
        timestamp, 
        prevBlockHash, 
        transactions, 
        index,
        address)
    block.calculateHash()
    timeStart = time()
    while(block.blockHash[0:block.difficulty] != ''.join(str(x) for x in np.zeros(block.difficulty, int))):
        block.nonce = block.nonce + 1
        block.timestamp = datetime.fromtimestamp(time()).isoformat() + "Z"
        block.calculateHash()
        # print(str(block.nonce) + "\t=>\t" + str(block.blockHash))
    minedBlock = block.minedBlock()
    return minedBlock

def applyWorker(function, blockData, address):
    q = Queue()
    workers = []
    for process in range(4):
        worker = Worker(target=function, name='process_{}'.format(process), args=(blockData, (process*1000)**2, address), queue=q)
        workers.append(worker)
        worker.start()

    result = q.get()
    if(result):
        for worker in workers:
            worker.terminate()
            print('{} Has been terminated'.format(worker.name))
        return result

def startMining(address):
    blockData = getJobs(address)
    print("IT goes here: ", blockData)
    result = applyWorker(mine, blockData, address)
    if (result):
        # print(result)
        submitMinedBlock(result)



if __name__ == '__main__':
    address = input("Enter address: ")
    while address is not None:
        startMining(address)
        break