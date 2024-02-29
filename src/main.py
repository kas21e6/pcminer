import io
import time
import traceback

from bitcoin.core import CBlock, CBlockHeader
from bitcoinrpc.authproxy import JSONRPCException
from rich import print

from Connection import Connection
from create_coinbase import create_coinbase
from get_merkle_root import get_merkle_root
from Miner import Miner


class PcMiner:
    def __init__(self):
        connection = Connection()
        self.connection = connection.connect()

    def run(self):
        print("PcMiner is running")

        try:
            block_template = self.connection.getblocktemplate(
                {"mode": "template", "rules": ["segwit"]}
            )

            tx = create_coinbase(
                block_template["height"], block_template["coinbasevalue"]
            )
            merkle_root = get_merkle_root([tx])
            timestamp = int(time.time())

            # Create block header
            header = CBlockHeader(
                4,
                bytes.fromhex(block_template["previousblockhash"])[::-1],
                merkle_root,
                timestamp,
                int(block_template["bits"], 16),
                0,
            )

            # Find the winning nonce
            miner = Miner()
            winning_block_header, _hash = miner.mine(header, block_template["target"])

            # Create the block
            block = CBlock(
                winning_block_header.nVersion,
                winning_block_header.hashPrevBlock,
                winning_block_header.hashMerkleRoot,
                winning_block_header.nTime,
                winning_block_header.nBits,
                winning_block_header.nNonce,
                [tx],
            )

            f = io.BytesIO()
            block.stream_serialize(f)
            serialized_block = f.getvalue()

            print("Serialized block: ", serialized_block.hex())

            submission = self.connection.submitblock(serialized_block.hex())

            print("Block submission result: ", submission)

        except JSONRPCException as json_exception:
            print("A JSON RPC Exception occurred: ", json_exception)
        except Exception as general_exception:
            print("An error occurred: ", general_exception)
            traceback.print_exc()


if __name__ == "__main__":
    app = PcMiner()
    app.run()
