import hashlib
import struct
import traceback


class Miner:
    def __init__(self, hex_bits: str):
        self.hex_bits = hex_bits
        self.target = self._calc_target_difficulty(hex_bits)

    def mine(self, header: object) -> bytes:
        try:
            nonce = header["nonce"]

            while nonce < 0x100000000:
                hash = self._double_hash(self._serialize_header(header, nonce))
                print("Hash:", hash[::-1].hex())
                print("With nonce", nonce)

                if hash[::-1] < self.target:
                    print("Success with nonce", nonce)
                    break

                nonce += 1
        except Exception as e:
            print("Error:", e)
            traceback.print_exc()

    def _double_hash(self, data: bytes) -> bytes:
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()

    def _serialize_header(self, header: object, nonce: int) -> bytes:
        return (
            struct.pack("<L", header["version"])
            + bytes.fromhex(header["prev_block"])[::-1]
            + header["merkle_root"][::-1]
            + struct.pack("<LLL", header["time"], int(header["bits"], 16), nonce)
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
