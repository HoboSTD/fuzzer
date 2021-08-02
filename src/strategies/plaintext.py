"""
Handles plaintext inputs.
"""

from src.parameters.parameter import Parameter
from src.parameters.parameter_type import get_parameter_type
from src.strategies.overflow import Overflow
from typing import List
from src.strategies.strategy import Strategy
from src.samples.sample import Sample

class PlainText(Strategy):

    def __init__(self) -> None:
        super().__init__()

    def set_sample(self, sample: Sample) -> None:
        """
        Splits the plaintext up into lines that use the overflow strategy.
        """
        super().set_sample(sample)

        lines = self._sample._input.splitlines()

        self._lines: List[Parameter] = [get_parameter_type(lines[i]) for i in range(0, len(lines))]

    def get_input(self) -> bytes:
        return b"\n".join([line.get_mutation() for line in self._lines])

    def get_keywords(self) -> List[bytes]:
        return [b"\n", b"\x00", b"\r\n", b"\t", b"\b", b"%s"]
