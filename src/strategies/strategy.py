"""
Interface for what strategies should implement.
"""

from src.samples.sample import Sample
from typing import List

class Strategy():

    def __init__(self) -> None:
        pass

    def set_sample(self, sample: Sample) -> Sample:
        self._sample = sample

    def get_input(self) -> bytes:
        """Returns an input that the fuzzer can use."""
        pass

    def get_keywords(self) -> List[bytes]:
        pass
