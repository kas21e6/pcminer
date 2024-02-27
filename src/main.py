import io
import time
from pprint import pprint

from bitcoinrpc.authproxy import JSONRPCException
from rich import print
from bitcoin.core import CBlockHeader, CBlock

from Connection import Connection
from Miner import Miner
from create_coinbase import create_coinbase
from get_merkle_root import get_merkle_root


class PcMiner:
    def __init__(self):
        connection = Connection()
        self.connection = connection.connect()

    def run(self):
        print("PcMiner is running")
        try:
            info = self.connection.getblocktemplate(
                {"mode": "template", "rules": ["segwit"]}
            )

            tx = create_coinbase(info["height"], info["coinbasevalue"])

            merkle_root = get_merkle_root([tx])

            print("Merkle root: ", merkle_root.hex())

            # Get current timestamp
            timestamp = int(time.time())

            # Create block header
            header = CBlockHeader(
                2,
                bytes.fromhex(info["previousblockhash"])[::-1],
                merkle_root[::-1],
                timestamp,
                int(info["bits"], 16),
                0,
            )

            # Find the winning nonce
            miner = Miner(info["bits"])
            version, prev_block, merkle_root, time_, bits, nonce = miner.mine(header)

            # Create the block
            block = CBlock(
                version, prev_block, merkle_root[::-1], time_, bits, nonce, [tx]
            )

            # Submit the block
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


if __name__ == "__main__":
    app = PcMiner()
    app.run()
