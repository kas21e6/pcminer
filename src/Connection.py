from bitcoinrpc.authproxy import AuthServiceProxy


class Connection:
    def __init__(self):
        self.rpc_user = "a"
        self.rpc_password = "b"
        self.rpc_host = "localhost"
        self.rpc_port = "8332"  # default port for Bitcoin's mainnet

    def connect(self):
        return AuthServiceProxy(
            f"http://{self.rpc_user}:{self.rpc_password}@{self.rpc_host}:{self.rpc_port}"
        )
