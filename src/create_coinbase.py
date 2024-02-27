from bitcoin.core import COutPoint, CTransaction, CTxIn, CTxOut
from bitcoin.wallet import CBitcoinAddress


def create_coinbase(block_height, output_value):
    # block_height as bytes
    block_height_bytes = block_height.to_bytes(4, byteorder="little")
    # size of block_height as bytes
    size_block_height = len(block_height_bytes).to_bytes(1, byteorder="little")
    arbitrary_data = b"Mined by a pleb"
    coinbase_scriptSig = size_block_height + block_height_bytes + arbitrary_data

    coinbase_input = CTxIn(COutPoint(), coinbase_scriptSig, 0xFFFFFFFF)

    scriptPubKey = CBitcoinAddress(
        "1C7zdTfnkzmr13HfA2vNm5SJYRK6nEKyq8"
    ).to_scriptPubKey()
    output_value = int("0x58f2fa00", 16)  # Convert hex to int
    coinbase_output = CTxOut(output_value, scriptPubKey)

    return CTransaction([coinbase_input], [coinbase_output], 0, 1)
