class Miner:
    @staticmethod
    def calc_target_difficulty(hex_bits: str) -> bytes:
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
