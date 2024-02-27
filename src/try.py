import binascii


def decode_coinbase_scriptsig(hex_string):
    script_sig_bytes = binascii.unhexlify(hex_string)
    size_block_height = script_sig_bytes[0]
    block_height_bytes = script_sig_bytes[1 : 1 + size_block_height]
    block_height = int.from_bytes(block_height_bytes, byteorder="little")

    # The rest of the scriptSig might contain arbitrary data
    arbitrary_data = script_sig_bytes[1 + size_block_height :]

    return block_height, arbitrary_data


coinbase_scriptSig_hex = "03d71b07254d696e656420627920416e74506f6f6c20626a31312f4542312f4144362f43205914293101fabe6d6d678e2c8c34afc36896e7d9402824ed38e856676ee94bfdb0c6c4bcd8b2e5666a0400000000000000c7270000a5e00e00"

block_height, arbitrary_data = decode_coinbase_scriptsig(coinbase_scriptSig_hex)

print(f"Block Height: {block_height}")
# print(f"Arbitrary Data (hex): {binascii.hexlify(arbitrary_data).decode()}")
print(f"Arbitrary Data (hex): {arbitrary_data.decode('ascii', 'ignore')}")
