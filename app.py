import requests, json,  np, threading, hashlib, binascii
from time import time
from Block import *
from Worker import *

workers = []
def getJobs(address):
    jobs = requests.get('https://stormy-everglades-34766.herokuapp.com/mining/get-mining-job/'+address)
    result = jobs.json()
    return result

def mine(blockData, nonce):
    blockDataHash = blockData['blockDataHash']
    difficulty = blockData['difficulty']
    timestamp = time()/1000
    block = Block(blockDataHash, difficulty, nonce, timestamp)
    block.calculateHash()
    timeStart = time()
    while(block.blockHash[0:block.difficulty] != ''.join(str(x) for x in np.zeros(block.difficulty, int))):
        block.nonce = block.nonce + 1
        block.timestamp = time()/1000
        block.calculateHash()
        # print(str(block.nonce) + "\t=>\t" + str(block.blockHash))
    
    print(time() - timeStart)
    print('\nSuccessful: '+str(block.blockHash))
    minedBlock = block.minedBlock()
    return minedBlock

def applyWorker(function, blockData):
    q = Queue()
    for process in range(4):
        worker = Worker(target=function, name='process_{}'.format(process), args=(blockData, (process*1000)**2), queue=q)
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
    result = applyWorker(mine, blockData)

if __name__ == '__main__':
    address = input("Enter address: ")
    while address is not None:
        startMining(address)
        break