#!/usr/bin/env python3
import hashlib
import json
from time import time

class User:
    def __init__(self):
        # Set up account and deposit
        self.name = input("username:")
        self.balance = int(input("deposit:"))

class Transaction:
    def __init__(self):
        sender = input("sender: ") 
        receiver = input("receiver: ")
        amount = int(input("amount: "))
        self.trans = {
                "sender": sender,
                "receiver": receiver,
                "amount": amount,
        }

    def verify(self, user_list):
        for user in user_list:
            if self.trans["sender"] == user.name:
                if self.trans["amount"] > user.balance:
                    print("error: not enough deposit")
                    return False
                else:
                    user.balance -= self.trans["amount"]
                    print(f"{user.name}: your balance is : {user.balance}")
                    return True
        # Unrecognized user
        print("error:unrecognized user")
        return False

    def show(self):
        print("class Transaction init:",self.trans["sender"], "sent", self.trans["receiver"], "BTC to", self.trans["amount"])


class Blockchain():
    def __init__(self):
        '''
        - current_transactions[]: list of transactions that will
                be added to the next block
        - chain[]: list of blocks in the blockchain
        '''
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block()

    def new_block(self):
        # Create a new block
        if len(self.chain) == 0:
            prev_proof = 0
            trans = []
        else:
            prev_proof = self.chain[-1]["proof"]
            trans = self.current_transactions
            if len(trans) == 0:
                print("error: no transaction to be added to a block")
                raise ValueError

        proof = self.proof_of_work()

        block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.current_transactions,
                'proof': proof,
                'previous_hash': prev_proof,
        }

        print(block)
        # Reset the current_transactions list
        self.current_transactions = []

        self.chain.append(block)
        print("A block has just been mined!")
        return block

    def new_transaction(self, user_list):
        # Add new transactions
        new_trans = Transaction()

        if not new_trans.verify(user_list):
            print("error: creating new transaction failed")
            return

        self.current_transactions.append(new_trans.trans)
        print("transaction added, not mined yet")
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Hash a block using sha-256
        block_string = json.dumps(block, sort_keys=True).encode()
        print("method hash:", hashlib.sha256(block_string).hexdigest())


    @property
    def last_block(self):
        # Return the last block
        return self.chain[-1]

    def proof_of_work(self):
        '''
        Find a p s.t. hash(p,p', hash) contains 4 leading zeros
        - p' is the previous hash
        - hash is this block hash
        '''
        if len(self.chain) == 0:
            last_proof = 0
            last_block = {}
        else:
            last_block = self.chain[-1]
            last_proof = last_block["proof"]
        cur_hash = self.hash 
        proof = 0
        while self.valid_proof(last_proof, proof, cur_hash) is False:
            proof += 1

        print(f"proof is :{proof}")
        return proof

    def valid_proof(self, last_proof, proof, cur_hash):
        '''
        Verify the hash contains 4 leading zeros
        '''
        guess = f'{last_proof}{cur_hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        if guess_hash[:4] == "0000":
            print(guess_hash)
        return guess_hash[:4] == "0000"

if __name__ == "__main__":
    user_list = []
    user = User()
    user_list.append(user)

    a = Blockchain()
    a.new_transaction(user_list)
    a.new_block()
