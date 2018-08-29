import hashlib, binascii
class Block:
    def __init__(self, blockDataHash, difficulty, nonce, timestamp):
        self.blockDataHash = blockDataHash
        self.difficulty = difficulty
        self.nonce = nonce
        self.timestamp = timestamp

    def calculateHash(self):
        data = str(self.blockDataHash) + "|" + str(self.timestamp) + "|" + str(self.nonce)
        self.blockHash = str(binascii.hexlify(hashlib.new('sha256', data.encode('utf8')).digest()).decode('utf8'))

    def minedBlock(self):
        return {
            'blockDataHash': self.blockDataHash,
            'dateCreated': self.timestamp,
            'nonce': self.nonce,
            'blockHash': self.blockHash
        }
