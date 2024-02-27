import hashlib
import io
import struct
import traceback
from bitcoin.core import CBlockHeader


class Miner:
    def __init__(self, hex_bits: str):
        self.hex_bits = hex_bits
        self.target = self._calc_target_difficulty(hex_bits)

    def mine(self, header: "CBlockHeader") -> bytes:
        version = header.nVersion
        prev_block = header.hashPrevBlock
        merkle_root = header.hashMerkleRoot
        time = header.nTime
        bits = header.nBits
        nonce = header.nNonce

        try:
            f = io.BytesIO()

            while nonce < 0x100000000:
                f.truncate(0)
                f.seek(0)

                serialized_data = self._serialize_header(
                    version, prev_block, merkle_root, time, bits, nonce
                )
                hash = self._double_hash(serialized_data)

                print("Hash:", hash[::-1].hex())
                print("With nonce", nonce)

                if hash[::-1] < self.target:
                    print("Success with nonce", nonce)
                    return (version, prev_block, merkle_root, time, bits, nonce)

                nonce += 1
        except Exception as e:
            print("Error:", e)
            traceback.print_exc()

    def make_block(version, prev_block, merkle_root, time, bits, nonce):
        return CBlockHeader(
            version,
            prev_block,
            merkle_root,
            time,
            bits,
            nonce,
        )

    def _double_hash(self, data: bytes) -> bytes:
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()

    def _serialize_header(
        self, version, prev_block, merkle_root, time, bits, nonce
    ) -> bytes:
        return (
            struct.pack(b"<i", version)
            + prev_block
            + merkle_root
            + struct.pack(b"I", time)
            + struct.pack(b"I", bits)
            + struct.pack(b"I", nonce)
        )

    def _calc_target_difficulty(self, hex_bits: str) -> bytes:
        """
        Decompress the target from a compact format.
        """
        bits = bytes.fromhex(hex_bits)

        # Extract the parts.
        byte_length = bits[0] - 3
        significand = bits[1:]

        # Scale the significand by byte_length.
        target = significand + b"\x00" * byte_length

        # Fill in the leading zeros.
        target = b"\x00" * (32 - len(target)) + target

        return target
