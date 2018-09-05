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
        self.blockHash = str(binascii.hexlify(hashlib.new('sha256', data.encode('utf8')).digest()).decode('utf8'))

    def minedBlock(self):
        date = datetime.fromtimestamp(time()).isoformat() + "Z"
        return {
            'blockHash': self.blockHash,
            'blockDataHash': self.blockDataHash,
            'nonce': self.nonce,
            'dateCreated': date,
            'minerAddress': self.minerAddress,
            'transactions': self.transactions,
            'index': self.index,
            'prevBlockHash': self.prevBlockHash,
            'difficulty': self.difficulty
        }
