import requests
from blockchain_module.models import blockModel, transactionsModel, blockchainModel, transactionStatusModel, blockStatusModel, merkelTreeHashesModel
import random
import json
import hashlib
from node_module.models import nodeModel
from django.middleware import csrf
from django.http import HttpResponse, HttpRequest


class Blockchain:
    def __init__(self):
        self.real_estate_chain = self.get_real_estate_chain()
        self.real_estate_transactions = self.get_real_estate_transactions()
        if len(self.real_estate_chain) == 0:
            self.create_genesis_block()

    # //////////////////////////////////////////////////

    def create_genesis_block(self):
        genesis_block_proof = 1
        previous_block_hash = "0x" + ('0' * 64)
        miner_address = self.real_estate_blockchain_system()["address"]
        genesis_block: blockModel = self.create_block(proof=genesis_block_proof,
                                                      previous_block_hash=previous_block_hash,
                                                      miner_address=miner_address)
        genesis_block_info: dict = genesis_block.block_information()
        genesis_block_info.pop("block_hash")
        # genesis_block_info["transactions"] = None
        genesis_block_hash = self.hash(
            block=genesis_block_info)
        genesis_block.block_hash = genesis_block_hash
        genesis_block.save()
        genesis_block_status: blockStatusModel = blockStatusModel.objects.create()
        genesis_block_status.block = genesis_block
        genesis_block_status.is_finalized = True
        genesis_block_status.save()

        # for field in genesis_block.block_status.all():
        #     field : blockStatusModel
        #     field.is_finalized = True
        #     field.save()

        self.real_estate_chain.append(genesis_block.block_information())
        self.real_estate_transactions = []

    # //////////////////////////////////////////////////

    def get_nodes(self) -> nodeModel:
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        return nodes

    # //////////////////////////////////////////////////

    def get_real_estate_chain(self):
        current_chain: blockModel = blockModel.objects.all()
        if current_chain is None:
            return []
        else:
            chain = []
            for block in current_chain:
                block: blockModel
                chain.append(block.block_information())
            return chain

    def get_real_estate_transactions(self):
        current_transactions: transactionsModel = transactionsModel.objects.filter(
            trx_status__published=False)
        if current_transactions is None:
            return []
        else:
            trxs = []
            for trx in current_transactions:
                trx: transactionsModel
                trxs.append(trx.transaction_information())
            return trxs

    def real_estate_blockchain_system(self) -> dict:
        system_blockchain: blockchainModel = blockchainModel.objects.filter(
            blockchain_name__iexact="real_estate_blockchain_system").first()
        if system_blockchain is None:
            new_system_blockchain: blockchainModel = blockchainModel.objects.create()
            new_system_blockchain.blockchain_name = "real_estate_blockchain_system"
            new_system_blockchain.blockchain_address = self.create_blockchain_address(
                blockchain_name="real_estate_blockchain_system")
            new_system_blockchain.save()
            system_blockchain = new_system_blockchain
        return {
            "name": system_blockchain.blockchain_name,
            "address": system_blockchain.blockchain_address,
            "inventory": system_blockchain.blockchain_inventory,
        }

    def create_blockchain_address(self, blockchain_name: str):
        sha512 = hashlib.sha512()
        sha512.update(blockchain_name.encode('utf-8'))
        sha512_digest = sha512.digest()
        blockchain_address = sha512_digest[-20:].hex()
        return f'0x{blockchain_address}({blockchain_name})'

    # ///////////////////////////////////////////////////////////////////

    def create_block(self,
                     proof,
                     previous_block_hash,
                     miner_address=None,
                     block_reward=0.0,
                     block_nonce=None
                     ):
        new_block: blockModel = blockModel.objects.create()
        new_block.block_number = len(self.real_estate_chain)+1
        new_block.mined_by = miner_address
        new_block.block_reward = block_reward
        new_block.previous_block_hash = previous_block_hash
        new_block.block_nonce = block_nonce
        new_block.block_proof_number = proof
        new_block.save()
        # self.real_estate_chain.append(new_block.block_information())
        # self.real_estate_transactions = []
        return new_block

    def get_last_block(self):
        return self.real_estate_chain[-1]

    def proof_of_work(self, previous_proof, new_proof=1):
        # print(f"new_proof_blockchain{new_proof}")
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**3 - previous_proof**3).encode()).hexdigest()

            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return {
            "new_proof": new_proof,
            "hash_operation": hash_operation[:10],
        }

# //////////////////////////////////////////////////////

    def choose_winner(*probabilities):
        rand = random.random()
        cumulative_probability = 0
        for i, probability in enumerate(probabilities[1]):
            cumulative_probability += probability
            if rand < cumulative_probability:
                return i

    def calculate_win_probabilities(*balances):
        total_balance = sum(balances[1])
        probabilities = [balance / total_balance for balance in balances[1]]
        return probabilities

    def proof_of_stake(self):
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        balances: list = []
        for node in nodes:
            node: nodeModel
            balances.append(float(node.node_inventory))
        probabilities: list = self.calculate_win_probabilities(balances)
        winner_id: int = self.choose_winner(probabilities)
        # print(winner_id)
        winner_node: nodeModel = nodes[winner_id]
        return winner_node
# /////////////////////////////////////////////////////////////////

    def hash(self, block: dict):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        hashed_block = hashlib.sha512(encoded_block).hexdigest()
        # print(hashed_block)
        return "0x" + hashed_block[:64]

    def transaction_hash(self, transaction: dict):
        encoded_transaction = json.dumps(transaction, sort_keys=True).encode()
        hashed_transaction = hashlib.sha512(encoded_transaction).hexdigest()
        # print(hashed_transaction)
        return "0x" + hashed_transaction[:64]

    def add_transaction(self, transaction_info: dict) -> dict:
        if transaction_info.get("transaction_type") == "miner_reward":
            new_transaction: transactionsModel = transactionsModel.objects.create()
            new_transaction.transaction_from_address = transaction_info.get(
                "new_trx").get("sender")
            new_transaction.transaction_to_address = transaction_info.get(
                "new_trx").get("receiver")
            new_transaction.transaction_value = float(transaction_info.get(
                "new_trx").get("value"))
            new_transaction.transaction_type = transaction_info.get(
                "transaction_type")

            new_transaction.save()

            new_transaction_status: transactionStatusModel = transactionStatusModel.objects.create()
            new_transaction_status.transaction = new_transaction
            new_transaction_status.save()

            return new_transaction

        elif transaction_info.get("transaction_type") == "tokenization":
            new_transaction: transactionsModel = transactionsModel.objects.create()
            new_transaction.transaction_from_address = transaction_info.get(
                "data").get("property_information").get("sender")
            new_transaction.transaction_to_address = transaction_info.get(
                "data").get("property_information").get("receiver")
            new_transaction.transaction_fee = transaction_info.get(
                "data").get("transaction_fee")
            new_transaction.transaction_type = transaction_info.get(
                "transaction_type")
            new_transaction.transaction_data = transaction_info.get(
                "token_id"
            )
            new_transaction.save()

            new_transaction_status: transactionStatusModel = transactionStatusModel.objects.create()
            new_transaction_status.transaction = new_transaction
            new_transaction_status.save()

            self.real_estate_transactions.append(
                new_transaction.transaction_information())
            # print(self.real_estate_transactions)
            previous_block = self.get_last_block()
            return {
                "block_index": int(previous_block["block_number"]) + 1,
                "transaction": new_transaction.transaction_information(),
            }

        elif transaction_info.get("transaction_type") == "buy_request":
            new_transaction: transactionsModel = transactionsModel.objects.create()
            new_transaction.transaction_from_address = transaction_info.get(
                "data").get("buy_request_information").get("sender")
            new_transaction.transaction_to_address = transaction_info.get(
                "data").get("buy_request_information").get("receiver")
            new_transaction.transaction_fee = transaction_info.get(
                "data").get("transaction_fee")
            new_transaction.transaction_type = transaction_info.get(
                "transaction_type")
            new_transaction.transaction_data = transaction_info.get(
                "data").get("buy_request_information").get("token_id")
            new_transaction.transaction_value = float(transaction_info.get(
                "transaction_prepayment"))

            new_transaction.save()

            new_transaction_status: transactionStatusModel = transactionStatusModel.objects.create()
            new_transaction_status.transaction = new_transaction
            new_transaction_status.save()

            self.real_estate_transactions.append(
                new_transaction.transaction_information())

            previous_block = self.get_last_block()

            return {
                "block_index": int(previous_block["block_number"]) + 1,
                "transaction": new_transaction.transaction_information(),
            }

        elif transaction_info.get("transaction_type") == "accept_buy_request":
            new_transaction: transactionsModel = transactionsModel.objects.create()
            new_transaction.transaction_from_address = transaction_info.get(
                "data").get("accept_reject_buy_request_information").get("sender")
            new_transaction.transaction_to_address = transaction_info.get(
                "data").get("accept_reject_buy_request_information").get("receiver")
            new_transaction.transaction_fee = transaction_info.get(
                "data").get("transaction_fee")
            new_transaction.transaction_type = transaction_info.get(
                "transaction_type")
            new_transaction.transaction_data = json.dumps(
                {
                    "token_id": transaction_info.get(
                        "data").get("accept_reject_buy_request_information").get("token_id"),
                    "status": "accepted",
                }
            )

            new_transaction.save()

            new_transaction_status: transactionStatusModel = transactionStatusModel.objects.create()
            new_transaction_status.transaction = new_transaction
            new_transaction_status.save()

            self.real_estate_transactions.append(
                new_transaction.transaction_information())

            previous_block = self.get_last_block()

            return {
                "block_index": int(previous_block["block_number"]) + 1,
                "transaction": new_transaction.transaction_information(),
            }

        elif transaction_info.get("transaction_type") == "reject_buy_request":
            new_transaction: transactionsModel = transactionsModel.objects.create()
            new_transaction.transaction_from_address = transaction_info.get(
                "data").get("accept_reject_buy_request_information").get("sender")
            new_transaction.transaction_to_address = transaction_info.get(
                "data").get("accept_reject_buy_request_information").get("receiver")
            new_transaction.transaction_fee = transaction_info.get(
                "data").get("transaction_fee")
            new_transaction.transaction_type = transaction_info.get(
                "transaction_type")
            new_transaction.transaction_data = json.dumps(
                {
                    "token_id": transaction_info.get(
                        "data").get("accept_reject_buy_request_information").get("token_id"),
                    "status": "rejected",
                }
            )

            new_transaction.save()

            new_transaction_status: transactionStatusModel = transactionStatusModel.objects.create()
            new_transaction_status.transaction = new_transaction
            new_transaction_status.save()

            self.real_estate_transactions.append(
                new_transaction.transaction_information())

            previous_block = self.get_last_block()

            return {
                "block_index": int(previous_block["block_number"]) + 1,
                "transaction": new_transaction.transaction_information(),
            }

        elif transaction_info.get("transaction_type") == "buy_operation":
            new_transaction: transactionsModel = transactionsModel.objects.create()
            new_transaction.transaction_from_address = transaction_info.get(
                "data").get("buy_operation_information").get("sender")
            new_transaction.transaction_to_address = transaction_info.get(
                "data").get("buy_operation_information").get("receiver")
            new_transaction.transaction_fee = transaction_info.get(
                "data").get("transaction_fee")
            new_transaction.transaction_type = transaction_info.get(
                "transaction_type")
            new_transaction.transaction_value = float(transaction_info.get(
                "data").get("remaining_cost"))
            new_transaction.transaction_data = json.dumps(
                {
                    "token_id": transaction_info.get("data").get("buy_operation_information").get("token_id"),
                    "operation": "buy_operation",
                }
            )

            new_transaction.save()

            new_transaction_status: transactionStatusModel = transactionStatusModel.objects.create()
            new_transaction_status.transaction = new_transaction
            new_transaction_status.save()

            self.real_estate_transactions.append(
                new_transaction.transaction_information())

            previous_block = self.get_last_block()

            return {
                "block_index": int(previous_block["block_number"]) + 1,
                "transaction": new_transaction.transaction_information(),
            }

        elif transaction_info.get("transaction_type") == "sell_operation":
            print("======================================================")
            print(transaction_info.get("buy_id"))
            new_transaction: transactionsModel = transactionsModel.objects.create()
            new_transaction.transaction_from_address = transaction_info.get(
                "data").get("sell_operation_information").get("sender")
            new_transaction.transaction_to_address = transaction_info.get(
                "data").get("sell_operation_information").get("receiver")
            new_transaction.transaction_fee = transaction_info.get(
                "data").get("transaction_fee")
            new_transaction.transaction_type = transaction_info.get(
                "transaction_type")
            new_transaction.transaction_data = json.dumps(
                {
                    "token_id": transaction_info.get("data").get("sell_operation_information").get("token_id"),
                    "buy_id": transaction_info.get("buy_id"),
                    "remaining_cost": transaction_info.get("remaining_cost"),
                    "operation": "sell_operation",
                }
            )

            new_transaction.save()

            new_transaction_status: transactionStatusModel = transactionStatusModel.objects.create()
            new_transaction_status.transaction = new_transaction
            new_transaction_status.save()

            self.real_estate_transactions.append(
                new_transaction.transaction_information())

            previous_block = self.get_last_block()

            return {
                "block_index": int(previous_block["block_number"]) + 1,
                "transaction": new_transaction.transaction_information(),
            }


# /////////////////////////////////////////////////////////////////


    def replace_chain(self):
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        longest_chain = None
        max_length = -1
        for node in nodes:
            node: nodeModel
            response = requests.get(f"{node.node_url}/get_chain/")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                # print(chain)
                if length > max_length:
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            for node in nodes:
                node: nodeModel
                csrf_token = csrf.get_token(request=HttpRequest())
                response = requests.post(
                    f"{node.node_url}/update_chain/",
                    data=json.dumps({"chain": longest_chain,
                                     "node_port": node.node_port}),
                    headers={"Content-Type": "application/json",
                             "X-CSRFToken": csrf_token})
                # print(response)
            # self.chain = longest_chain
            return True

        return False

    def replace_transactions(self, trx: dict, transactions=None):
        nodes: nodeModel = nodeModel.objects.filter(is_disable=False).all()
        for node in nodes:
            node: nodeModel
            csrf_token = csrf.get_token(request=HttpRequest())
            response = requests.post(
                url=f"{node.node_url}/update_transactions/",
                data=json.dumps({"transaction": trx,
                                 "transactions": transactions,
                                 "node_port": node.node_port, }),
                headers={"Content-Type": "application/json",
                         "X-CSRFToken": csrf_token}
            )
            if not response.json()["status"]:
                return False
        return True

    # ///////////////////////////////////////////////////////////

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            current_proof = current_block["proof"]
            hash_operation = hashlib.sha256(
                str(current_proof**3 - previous_proof**3).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                return False
            previous_block = current_block
            block_index += 1
        return True

    # /////////////////////////////////////////////////////////////////

    def merkel_tree_root_hash(self, hashes):
        print(hashes)
        if len(hashes) == 1:
            merkel_hash: merkelTreeHashesModel = merkelTreeHashesModel.objects.create()
            merkel_hash.current_hash = hashes[0]
            merkel_hash.save()
            return hashes[0]

        new_hashes = []
        for i in range(0, len(hashes)-1, 2):
            combined_hash: str = hashes[i] + hashes[i+1]
            new_hash = hashlib.sha512(
                combined_hash.encode('utf-8')).hexdigest()
            
            merkel_hash: merkelTreeHashesModel = merkelTreeHashesModel.objects.create()
            merkel_hash.current_hash = hashes[i]
            merkel_hash.combined_hash = hashes[i+1]
            merkel_hash.save()
            
            new_hashes.append(new_hash)

        if len(hashes) % 2 == 1:
            combined_hash = hashes[-1] + hashes[-1]
            new_hash = hashlib.sha512(
                combined_hash.encode('utf-8')).hexdigest()
            
            merkel_hash: merkelTreeHashesModel = merkelTreeHashesModel.objects.create()
            merkel_hash.current_hash = hashes[-1]
            merkel_hash.combined_hash = hashes[-1]
            merkel_hash.save()
            
            new_hashes.append(new_hash)

        return self.merkel_tree_root_hash(new_hashes)

    # def verify_transaction(transaction_hash, merkle_root, transaction_hashes):
    #     if transaction_hash in transaction_hashes and merkle_root == build_merkle_tree(transaction_hashes):
    #         return True
    #     return False

    # # Example usage
    # block_transaction_hashes = ["hash1", "hash2", "hash3", "hash4"]
    # merkle_root = build_merkle_tree(block_transaction_hashes)
    # transaction_hash_to_verify = "hash2"
    # is_valid = verify_transaction(transaction_hash_to_verify, merkle_root, block_transaction_hashes)
    # print(is_valid)


real_estate_blockchain: Blockchain = Blockchain()
