# A blockchain program in Python

# For timestamp
import datetime

# Calculating the hash
# in order to add digital
# fingerprints to the blocks
import hashlib

# To store data
# in our blockchain
import json

# Flask is for creating the web
# app and jsonify is for
# displaying the blockchain
from flask import Flask, jsonify

#create a class for your blockchain
class Blockchain:

    # create the function
    # to create the first block
    # set its hash to "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    # Create a function
    # to add more blocks
    # into the blockchain
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    # Create a function
    # to display the previous block
    def print_previous_block(self):
        return self.chain[-1]
    #create another function
    #to add more blocks
    def create_block1(self, proof, previous_hash):
        block1 = {'index': len(self.chain) + 1,
                  'timestamp': str(datetime.datetime.now()),
                  'proof': proof,
                  'previous_hash': previous_hash}
        self.chain.append(block1)
        return block1
    #Create another function to display the previous block into block1
    def print_previous_block1(self):
        return self.chain[-2]

    # Create a function for proof of work, this will be used to mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1

        return True


# Creating a web app using Flask
app = Flask(__name__)

# Create the object
# of the class blockchain
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    return jsonify(response), 200


# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Check if the blockchain is valid
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200


# Run the flask server locally
app.run(host='127.0.0.1', port=5000)
