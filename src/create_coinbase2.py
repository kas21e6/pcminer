from bitcoin.core import COutPoint, CTransaction, CTxIn, CTxOut
from bitcoin.core.script import CScript
from bitcoin.wallet import CBitcoinAddress, P2PKHBitcoinAddress
import binascii

# Transaction components based on your provided hex
# The scriptSig in the coinbase transaction's input usually includes block height and arbitrary data
coinbase_scriptSig_hex = "03d71b07254d696e656420627920416e74506f6f6c20626a31312f4542312f4144362f43205914293101fabe6d6d678e2c8c34afc36896e7d9402824ed38e856676ee94bfdb0c6c4bcd8b2e5666a0400000000000000c7270000a5e00e00"
# coinbase_scriptSig_bytes = binascii.unhexlify(coinbase_scriptSig_hex)
# decoded_message = coinbase_scriptSig_bytes.decode("utf-8")
# print("Decoded message:", decoded_message)
coinbase_scriptSig = bytes.fromhex(coinbase_scriptSig_hex)
scriptPubKey = CScript(
    bytes.fromhex("76a914338c84849423992471bffb1a54a8d9b1d69dc28a88ac")
)

# Coinbase input
# The outpoint is always null for coinbase transactions, and the scriptSig contains block height and extra nonce
coinbase_input = CTxIn(
    COutPoint(b"\x00" * 32, 0xFFFFFFFF), coinbase_scriptSig, 0xFFFFFFFF
)

# Output: sending the block reward to the miner's address
# The value is the block reward plus transaction fees (if any), here represented in satoshis
output_value = int("0x58f2fa00", 16)  # Convert hex to int
coinbase_output = CTxOut(output_value, scriptPubKey)

# Create the transaction
tx = CTransaction([coinbase_input], [coinbase_output], 0, 1)

# Transaction serialization
tx_hex = tx.serialize().hex()

print(tx_hex)
