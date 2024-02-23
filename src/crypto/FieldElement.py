from my_types import Number


class FieldElement:
    def __init__(self, num: int, prime: int):
        if num >= prime or num < 0:
            error = "Num {} not in field range 0 to {}".format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, FieldElement):
            return False

        return bool(self.num == other.num and self.prime == other.prime)

    def __ne__(self, other: object) -> bool:
        if other is None or not isinstance(other, FieldElement):
            return False

        return not self.__eq__(other)

    def __add__(self, other: "FieldElement"):
        if self.prime != other.prime:  # <1>
            raise TypeError("Cannot add two numbers in different Fields")

        num = (self.num + other.num) % self.prime  # <2>

        return self.__class__(num, self.prime)  # <3>

    def __sub__(self, other: "FieldElement"):
        if self.prime != other.prime:
            raise TypeError("Cannot subtract two numbers in different Fields")

        num = (self.num - other.num) % self.prime

        return self.__class__(num, self.prime)

    def __mul__(self, other: "FieldElement"):
        if self.prime != other.prime:
            raise TypeError("Cannot multiply two numbers in different Fields")

        num = (self.num * other.num) % self.prime

        return self.__class__(num, self.prime)

    def __pow__(self, exponent: int):
        n = exponent % (self.prime - 1)  # <1>
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other: "FieldElement"):
        if self.prime != other.prime:
            raise TypeError("Cannot divide two numbers in different Fields")

        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime

        return self.__class__(num, self.prime)
