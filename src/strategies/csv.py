"""
Handles csv inputs.
"""

from random import randint
from src.parameters.parameter_type import get_parameter_type
from src.strategies.overflow import Overflow
from typing import List
from src.samples.sample import Sample
from src.strategies.strategy import Strategy

class Csv(Strategy):
    
    def __init__(self) -> None:
        super().__init__()
    
    def get_keywords(self) -> List[bytes]:
        return [b",", b"\"", b"\'", b"%s", b"\n", b"\r\n"]

    def set_sample(self, sample: Sample) -> None:
        """
        Splits the csv text up into a 2d array. Each cell has a strategy in it that randomises that
        cells output.
        """

        super().set_sample(sample)

        self._csv = [[get_parameter_type(cell) for cell in line.split(b",")] for line in self._sample._input.splitlines()]

    def get_input(self) -> bytes:
        # sometimes just return the sample for bit-flipping
        do_normal = randint(0, 10) == 0
        if do_normal:
            return self._sample._input

        content = b""
        for i in range(0, len(self._csv)):
            for j in range(0, len(self._csv[i])):
                content += self._csv[i][j].get_mutation()
                if j != (len(self._csv[i]) - 1):
                    content += b","
            content += b"\n"

        return content
