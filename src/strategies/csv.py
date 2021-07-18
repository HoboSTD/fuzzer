"""
Handles csv inputs.
"""

from random import randint
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

        self._csv = [[create_cell(cell) for cell in line.split(b",")] for line in self._sample._input.splitlines()]

    def get_input(self) -> bytes:
        # sometimes just return the sample for bit-flipping
        do_normal = randint(0, 10) == 0
        if do_normal:
            return self._sample._input

        content = b""
        for i in range(0, len(self._csv)):
            for j in range(0, len(self._csv[i])):

                do_rand = randint(0, 5) == 0
                if do_rand:
                    content += self._csv[i][j].randomise_cell(self._csv[i][j].get_contents(), self.get_keywords())
                else:
                    content += self._csv[i][j].get_contents()
                if j != (len(self._csv[i]) - 1):
                    content += b","
            content += b"\n"

        return content

class CsvCell():

    def __init__(self, input: bytes) -> None:
        self._input = input
        self._overflow = Overflow(input)

    def get_contents(self) -> bytes:
        """Returns a random string based on the given input."""
        return self._overflow.get_input()

    def randomise_cell(self, cell: bytes, keywords: List[bytes]) -> bytes:
        """Returns a cell that has been randomised."""

        def rand_keyword():
            return keywords[randint(0, len(keywords) - 1)]

        nrands = randint(1, len(cell))
        for _ in range(0, nrands):
            index = randint(0, len(cell) - 1)

            cell = cell[0:index] + rand_keyword() + cell[index:]

        return cell

class CsvIntegerCell(CsvCell):

    def __init__(self, input: bytes) -> None:
        super().__init__(input)
        self._input = int(input.decode("utf-8"))
        self._int_max = 2**32
        self._int_min = -self._int_max

    def get_contents(self) -> bytes:
        """Returns a random integer for the csv cell."""

        return str(randint(self._int_min, self._int_max)).encode("utf-8")

def create_cell(input: bytes) -> CsvCell:
    """Returns a CsvCell based on what the input is"""

    if input.isdigit():
        return CsvIntegerCell(input)
    
    return CsvCell(input)
