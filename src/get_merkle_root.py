from bitcoin.core import CBlock


def get_merkle_root(txs) -> bytes:
    return CBlock.build_merkle_tree_from_txs(txs)[-1]
