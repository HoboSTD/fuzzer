"""
Handles plaintext inputs.
"""

from src.strategies.overflow import Overflow
from typing import List
from src.strategies.strategy import Strategy
from src.samples.sample import Sample

class PlainText(Strategy):

    def __init__(self) -> None:
        super().__init__()

    def set_sample(self, sample: Sample) -> None:
        super().set_sample(sample)
        # split it up into new lines
        lines = self._sample._input.splitlines()

        self._lines: List[Overflow] = []
        # get each one to be a buffer overflow strategy
        for i in range(0, len(lines)):
            self._lines.append(Overflow(lines[i]))

    def get_input(self) -> bytes:
        ret = b""
        for line in self._lines:
            ret = b"".join([ret, line.get_input(), b"\n"])
        return ret

    def get_keywords(self) -> List[bytes]:
        return [b"\n", b"\x00", b"\r\n", b"\t", b"\b", b"%s"]
