"""
Interface that all the other sample types follow.
"""

from typing import List

class Sample():

    def __init__(self, path: str) -> None:
        self._path: str = path
        self.load_file()

    def load_file(self) -> None:
        with open(self._path) as file:
            self._input: bytes = file.read().encode("utf-8")

    def get_keywords(self) -> List[bytes]:
        pass

