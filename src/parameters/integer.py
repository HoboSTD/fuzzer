"""
Generates random integers that are used during fuzzing.
"""

from random import randint

class Integer():

    def __init__(self) -> None:
        self._int_max = 2**30
        self._int_min = -self._int_max

    def get_mutation(self) -> bytes:
        """
        Returns a random integer in the defined range.
        """

        return str(randint(self._int_min, self._int_max)).encode("utf-8")
