import hashlib
from typing import List


def calc_merkle_root(transactions):
    # Convert transactions into big-endian bytes.
    be_hashes = [
        bytes.fromhex(transaction.raw_hex())[::-1] for transaction in transactions
    ]

    # We combine the hashes pairwise until there is only 1 left.
    while len(be_hashes) > 0:

        # Duplicate the last hash if the list size is odd.
        if len(be_hashes) % 2 != 0:
            be_hashes.append(be_hashes[-1])

        # Combine the hashes pairwise.
        for i in range(len(be_hashes) // 2):
            concat_hash = be_hashes[i * 2] + be_hashes[i * 2 + 1]
            be_hash = hashlib.sha256(hashlib.sha256(concat_hash).digest()).digest()
            be_hashes[i] = be_hash

        be_hashes = be_hashes[: len(be_hashes) // 2]

    return be_hashes[0][::-1].hex()
