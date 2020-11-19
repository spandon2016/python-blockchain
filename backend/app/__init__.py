import os
import random

from flask import Flask, jsonify

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub



app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)




@app.route('/')
def default():
    return "Welcome to the blockchain"

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())
#return blockchain.__repr__()

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = "stubbed_transaction_data"

    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)

    return jsonify(block.to_json())


PORT = 5000
if os.environ.get('PEER') == 'True':
    print("inside environ")
    PORT = random.randint(5001, 6000)

print("afer if")
app.run(port=PORT)



