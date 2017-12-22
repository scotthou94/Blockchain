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
                return

        proof = self.proof_of_work()

        block = {
                'block_index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.current_transactions,
                'proof': proof,
                'previous_hash': prev_proof,
        }

        # Reset the current_transactions list
        self.current_transactions = []

        self.chain.append(block)
        if len(self.chain) > 1:
            print(f"block #{len(self.chain)} has just been mined!")
        return block

    def new_transaction(self, user_list):
        # Add new transactions
        new_trans = Transaction()

        if not new_trans.verify(user_list):
            print("error: creating new transaction failed")
            return

        self.current_transactions.append(new_trans.trans)
        print("transaction added, not mined yet")
        return self.last_block['block_index'] + 1

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

        #print(f"proof is :{proof}")
        return proof

    def valid_proof(self, last_proof, proof, cur_hash):
        '''
        Verify the hash contains 4 leading zeros
        '''
        guess = f'{last_proof}{cur_hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        '''
        if guess_hash[:4] == "0000":
            print(guess_hash)
        '''
        return guess_hash[:4] == "0000"

def setup_user(user_list):
    new_user = User()
    user_list.append(new_user)

def new_trans(user_list, chain):
    chain.new_transaction(user_list)

def mine_block(chain):
    chain.new_block()

def show_block(chain):
    print(chain.last_block)

def show_chain(chain):
    for block in chain.chain:
        print(f"{block}")


if __name__ == "__main__":
    prompt = '''
    *************** Welcome to our blockchain system *******************
    Pleas select the following operations
    1. Setup user name and initial depost
    2. New transactions
    3. Mine the block
    4. Show the latest block
    5. Show the current chain
    6. Quit
    ********************************************************************
    '''
    print(prompt)
    user_list = []
    blockchain = Blockchain()
    while True:
        choice = int(input("Your operation:"))
        if choice == 1:
            setup_user(user_list)
        elif choice == 2:
            new_trans(user_list, blockchain)
        elif choice == 3:
            mine_block(blockchain)
        elif choice == 4:
            show_block(blockchain)
        elif choice == 5:
            show_chain(blockchain)
        elif choice == 6:
            break
        else:
            print("Please enter a valid choice")
            continue


        '''
        user = User()
        user_list.append(user)
        a.new_transaction(user_list)
        a.new_block()
        '''
