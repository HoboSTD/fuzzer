"""
Overflow stuff idk.
"""

from random import randint
from typing import List
from src.strategies.strategy import Strategy

class Overflow(Strategy):
    
    def __init__(self, base: bytes) -> None:
        self._base = base
        self._mult = 0

    def get_input(self) -> bytes:
        """
        Returns a random overflow type thing.
        """

        rand = randint(0, 2)
        if rand == 0:
            return self._base
        elif rand == 1:
            self._mult += 1
            return self._base * self._mult
        elif rand == 2:
            return self._mult * b"%s"
        
        return self._base * self._mult + self._mult * b"%s"


    def get_keywords(self) -> List[bytes]:
        return [b"%s"]
