"""
Generates random strings that are used during fuzzing.
"""

from random import randint

class String():

    def __init__(self, base: bytes) -> None:
        self._base: bytes = base

    def get_mutation(self) -> bytes:
        """
        Either returns the base string or a really large string.
        """
        
        rand = randint(0, 200)

        if rand <= 199:
            return self._base
        else:
            # this could be expanded to return a random string based on some keywords
            return b"%s" * 1000
