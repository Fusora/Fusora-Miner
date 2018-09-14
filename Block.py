import hashlib, binascii
from time import time
from datetime import datetime
class Block:
    def __init__(self, blockDataHash, difficulty, nonce, timestamp, prevBlockHash, transactions, index, minerAddress):
        self.blockDataHash = blockDataHash
        self.difficulty = difficulty
        self.nonce = nonce
        self.timestamp = timestamp
        self.prevBlockHash = prevBlockHash
        self.transactions = transactions
        self.index = index
        self.minerAddress = minerAddress

    def calculateHash(self):
        data = str(self.blockDataHash) + "|" + str(self.timestamp) + "|" + str(self.nonce)
        # print(hashlib.sha256(data))
        self.blockHash =  hashlib.sha256(data.encode('utf8')).hexdigest()

    def minedBlock(self):
        return {
            'blockHash': self.blockHash,
            'blockDataHash': self.blockDataHash,
            'nonce': self.nonce,
            'dateCreated': self.timestamp,
            'minerAddress': self.minerAddress,
            'transactions': self.transactions,
            'index': self.index,
            'prevBlockHash': self.prevBlockHash,
            'difficulty': self.difficulty
        }
