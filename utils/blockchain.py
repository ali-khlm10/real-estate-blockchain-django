

class Blackchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0' * 64)
        self.nodes = set()
