import hashlib
import time
from pprint import pprint

from bitcoinlib.transactions import Transaction
from bitcoinlib.blocks import Block
from bitcoinrpc.authproxy import JSONRPCException
from rich import print

from Connection import Connection
from Miner import Miner


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

            # print(
            #     "difficulty: ",
            #     Miner.calc_target_difficulty(info["bits"]).hex(),
            # )
            # print(
            #     "coinbase value: ",
            #     info["coinbasevalue"],
            # )
            # print("previous block hash: ", info["previousblockhash"])
            # print("height: ", info["height"])

            # Create the Coinbase Transaction
            tx = Transaction(coinbase=False)
            tx.add_input(
                "0000000000000000000000000000000000000000000000000000000000000000",
                0,
                sequence=0xFFFFFFFF,
                index_n=0xFFFFFFFF,
            )
            tx.add_output(info["coinbasevalue"], "1runeksijzfVxyrpiyCY2LCBvYsSiFsCm")

            # Calculate the Merkle Root
            merkle_root = hashlib.sha256(
                hashlib.sha256(bytes.fromhex(tx.raw_hex())).digest()
            ).digest()

            # Get current timestamp
            timestamp = int(time.time())
            print("timestamp: ", timestamp)

            print("merkle root: ", merkle_root.hex())

            # Create block header
            header = {
                "version": 2,
                "prev_block": info["previousblockhash"],
                "merkle_root": merkle_root,
                "time": timestamp,
                "bits": info["bits"],
                "nonce": 0,
            }

            # pprint(header)

            # Mine the block
            miner = Miner(info["bits"])
            winning_nonce, winning_hash = miner.mine(header)

            block = Block(
                block_hash=winning_hash.hex(),
                version=header["version"],
                prev_block=header["prev_block"],
                merkle_root=header["merkle_root"],
                time=header["time"],
                bits=header["bits"],
                nonce=winning_nonce,
                height=info["height"],
            )

            pprint(block.as_dict())

            # Create the block

        except JSONRPCException as json_exception:
            print("A JSON RPC Exception occurred: ", json_exception)
        except Exception as general_exception:
            print("An error occurred: ", general_exception)


if __name__ == "__main__":
    app = PcMiner()
    app.run()
