""" This is block chain program with python3 """

import json
import hashlib
import sys
from time import time
from uuid import uuid4
from flask import Flask, jsonify


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
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ define """

    @staticmethod
    def valid_proof(last_proof, proof):
        """ this is a function that cpu is work """
        this_proof = f'{proof}{last_proof}'.encode()
        this_proof_hash = hashlib.sha256(this_proof).hexdigest()
        deficulty = "00000"
        return this_proof_hash[:5] == deficulty

    def proof_of_work(self, last_proof):
        """ POW """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof


app = Flask(__name__)

node_id = str(uuid4())

block_chanin = BlockChain()


@app.route("/mine")
def mine():
    """ this function mine a block and add it the chain """
    return "Hello"


@app.route("/trxs/new", methods=['POST'])
def new_trx():
    """ add a transaction """
    return "new  transaction"


@app.route('/chain')
def full_chain():
    ''' jskfskjf '''
    res = {
        'chain': block_chanin.chain,
        'length': len(block_chanin.chain),
    }
    return jsonify(res), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=sys.argv[1])
