"""
Overflow stuff idk.
"""

from random import randint
from typing import List
from src.strategies.strategy import Strategy

class Overflow(Strategy):
    
    def __init__(self, base: bytes) -> None:
        self._base = base
        self._mult = 1

    def get_input(self) -> bytes:
        """
        Returns a random overflow type thing.
        """

        rand = randint(0, 200)
        if rand <= 199:
            return self._base
        else:
            return b"%s" * 10000


    def get_keywords(self) -> List[bytes]:
        return [b"%s"]
