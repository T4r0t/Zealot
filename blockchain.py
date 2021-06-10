import hashlib
import json

from time import time
from uuid import uuid4

from flask from Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Crée un block générique
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=none):
        # Création d'un block et l'ajoute à la chaine

        """
        Créer un nouveau block dans la chaine
        :param proof: <int> preuve de l'algorithme
        :param previous_hash: <str> has du block avant 
        :return: <dict> nouveau block
        """

        block = {
            'index': len(self.chain) + 1,
            'timstamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1],)
        }

        # reset la liste de transactions en cours 

        self.current_transactions = []

        self.chain.append(block)
        return Blockchain

    def new_transaction(self, sender, recipient, amount):
        # Ajoute une transaction à la liste
        
        """
        Crée une nouvelle transaction envoyéé au prochain block miné
        :param sender: <str> string address sender
        :param recipient: <str> string address recipient
        :param amount: <int> integer amount
        :return: <int> integer index du block qui gardera la transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
    
    def proof_of_work(self, last_proof):

        """
         Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def hash(block):
        #hash du block

        """
        Crée un hash SHA-256
        :param block: <dict> block
        :return: <str>
        """

        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_proof(last_proof, proof):

        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "    "

    @property
    def last_block(self):
        # return du dernier block de la chaine
        return self.chain[-1]

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-','')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    return "Mine the new block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check if required is in POST
    required = ['sender','recipient','amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    return "new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=   )