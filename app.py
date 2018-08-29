import requests, json,  np, threading
from time import time
from multiprocessing import Process, Queue
from Block import *
from Worker import *
from flask import Flask

app = Flask(__name__)
workers = []



def getJobs(address):
    # jobs = {
    #     'difficulty': 5,
    #     'blockDataHash': "00004b611759df07b5a81d0cac07f2174c965bb6bced97c7f63325678a0189a2"
    # }
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

    for worker in workers:
        worker.start()

    result = q.get()
    if(result):
        for worker in workers:
            worker.terminate()
            print('{} Has been terminated'.format(worker.name))
        return result

def sendRequest(req):
    jobs = requests.get('https://stormy-everglades-34766.herokuapp.com/mining/get-mining-job/'+address)

@app.route('/')
def index():
    validAddress = 'a44f70834a711F0DF388ab016465f2eEb255dEd0'.lower()
    blockData = getJobs(validAddress)
    result = applyWorker(mine, blockData)
    return str(result)
    

if __name__ == '__main__':
    app.run()
        