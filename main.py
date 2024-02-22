from bitcoinrpc.authproxy import JSONRPCException
from rich import print
from Miner import Miner
from Connection import Connection


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
            print(
                "Connected to Bitcoin network: ",
                Miner.calc_target_difficulty(info["bits"]).hex(),
            )
        except JSONRPCException as json_exception:
            print("A JSON RPC Exception occurred: ", json_exception)
        except Exception as general_exception:
            print("An error occurred: ", general_exception)


if __name__ == "__main__":
    app = PcMiner()
    app.run()
