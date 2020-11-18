""" This is block chain program with python3 """

import json
import hashlib
import sys
import requests
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request


class BlockChain():
    """define a block chain on one machin"""

    def __init__(self):
        self.current_trxs = []
        self.chain = []
        self.nodes = set()
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

    def register_node(self, address):
        """ node's """
        parsed_url = urlpars(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """ chick if the chain is valid """
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self):
        """ checs all nodes and selecs the best chain """
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)
        for node in neighbours:
            response = request.get(f'http://{node}/chain')
            if response.status_code == 200:
                lenght = response.json()['length']
                chain = response.json()['chain']
                if lenght > max_length and self.valid_chain(chain):
                    max_length = lenght
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False


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
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['trxs'],
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


@app.route('/nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')
    for node in nodes:
        BlockChain.register_node(node)

    res = {"message":"nodes added","total_nodes": list(BlockChain.nodes)}

    return jsonify(res), 201

@app.route('/nodes/resolve')
def consensus():
    replaced = BlockChain.resolve_conflicts()
    if replaced:
        res = {
           "message":'replaced',
            'new_chain':blockChain.chain,
        }
    else:
        res = {'message':'I am the best','chain':blockChain.chain}
    return jsonify(res), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=sys.argv[1])
