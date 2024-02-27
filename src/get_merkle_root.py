from bitcoin.core import CBlock, CTransaction, b2lx
from bitcoin.core.script import OP_CHECKSIG, OP_DUP, OP_EQUALVERIFY, OP_HASH160, CScript
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress


def get_merkle_root(txs):
    return CBlock.build_merkle_tree_from_txs(txs)[-1]
