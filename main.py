""" This is block chain program with python3 """

import json
import hashlib
from time import time


class BlockChain():
    """define a block chain on one machin"""

    def __init__(self):
        self.chain = []
        self.new_block(previous_hash=1, proof=100)
        self.current_trxs = []

    def new_block(self, proof, previous_hash=None):
        """ creat a new block """
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "trxs": self.current_trxs,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }
        self.current_trxs = []
        self.chain.append(block)

        return block

    def new_trx(self, sender, recipient, amount):
        """ add new trx to the mempool  """
        self.current_trxs.append(
            {"sender": sender, "recipient": recipient, "amount": amount})

    @staticmethod
    def hash(block):
        """ hash a block """
        block_string = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ define """
