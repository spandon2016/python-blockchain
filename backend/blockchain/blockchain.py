from backend.blockchain.Block import Block


class Blockchain:
    """
    Blockchain a public ledger of transactions
    Implemented as list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]



    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """ 
        Replace the local chain with the incoming one if the following applies:
        -- The incoming chain is longer than the last one
        -- the incoming chain is formatted properly
        """
        if len(chain) <= len(self.chain):
            raise Exception('Cannot relpace. The incoming chain must be longer')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception (f'Cannot replay. The incoming chain is invalid {e}')

        self.chain = chain


    def to_json(self):
        """ 
        Serialize the blockchain into a list of blocks.
        """
        """
        serialzed_chain = []

        for block in self.chain:
            serialzed_chain.append(block.to_json())


        return serialzed_chain
        """
        return list(map(lambda block: block.to_json(), self.chain))

    

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
        - the chain must start with the genesis block
        - blocks must be formatted correctly
        """

        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        n = len(chain)

        for i in range(1, n):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)

def main():

    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)
    print(f'blockhain.py __name__: {__name__}')

if __name__ == '__main__':
    main()
