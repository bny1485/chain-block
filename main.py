""" This is block chain program with python3 """

import json
import hashlib
import sys
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class BlockChain():
    """define a block chain on one machin"""

    def __init__(self):
        self.chain = []
        self.current_trxs = []
        self.new_block(previous_hash=1, proof=100)

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

        return self.last_block['index']+1

    @staticmethod
    def hash(block):
        """ hash a block """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ define """
        return self.chain[-1]

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

blockChain = BlockChain()


@app.route("/mine", methods=['GET'])
def mine():
    """ this function mine a block and add it the chain """
    last_block = blockChain.last_block
    # last_proof = last_proof['proof']
    proof = blockChain.proof_of_work(last_block)

    blockChain.new_trx(sender="0", recipient=node_id, amount=50)
    previous_hash = blockChain.hash(last_block)
    block = blockChain.new_block(proof, previous_hash)

    response = {
        'message': "new block froged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route("/trxs/new", methods=['POST'])
def new_trx():
    """ add a transaction """
    values = request.get_json()
    this_block = blockChain.new_trx(
        values['sender'], values['recipient'], values['amount'])
    res = {"message": f"will be added to block {this_block}"}
    return jsonify(res), 201


@app.route('/chain')
def full_chain():
    ''' number of chain '''
    res = {
        'chain': blockChain.chain,
        'length': len(blockChain.chain),
    }
    return jsonify(res), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=sys.argv[1])
