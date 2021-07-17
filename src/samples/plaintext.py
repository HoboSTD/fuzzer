"""
Type for the plaintext files.
"""

from typing import List
from src.samples.sample import Sample

class PlainText(Sample):
    
    def get_keywords(self) -> List[bytes]:
        return [b"\n", b"\x00", b"\r\n", b"\t", b"\b", b"%s"]

    
