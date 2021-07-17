"""
Handles plaintext inputs.
"""

from typing import List
from src.strategies.strategy import Strategy

class PlainText(Strategy):

    def __init__(self) -> None:
        super().__init__()

    def get_input(self) -> bytes:
        return super().get_input()

    def get_keywords(self) -> List[bytes]:
        return [b"\n", b"\x00", b"\r\n", b"\t", b"\b", b"%s"]
