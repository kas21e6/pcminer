import io
import struct
import traceback
from typing import cast

from bitcoin.core import CBlockHeader, Hash


class Miner:
    def mine(self, header: "CBlockHeader", target: str) -> tuple[CBlockHeader, bytes]:
        version = cast(int, header.nVersion)
        prev_block = cast(bytes, header.hashPrevBlock)
        merkle_root = cast(bytes, header.hashMerkleRoot)
        time = cast(int, header.nTime)
        bits = cast(int, header.nBits)
        nonce = cast(int, header.nNonce)
        bTarget = bytes.fromhex(target)

        try:
            f = io.BytesIO()

            while nonce < 0x100000000:
                f.truncate(0)
                f.seek(0)

                serialized_data = self._serialize_header(
                    version, prev_block, merkle_root, time, bits, nonce
                )
                hash = Hash(serialized_data)

                print("Hash:", hash[::-1].hex())
                print("With nonce", nonce)

                if hash[::-1] < bTarget:
                    print("Success with nonce", nonce)

                    return (
                        CBlockHeader(
                            version, prev_block, merkle_root, time, bits, nonce
                        ),
                        hash,
                    )

                nonce += 1

            return (header, b"")
        except Exception as e:
            print("Error:", e)
            traceback.print_exc()
            return (header, b"")

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
