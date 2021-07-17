"""
Trying to fix circular imports
"""

from src.samples.sample import Sample
from src.samples.sample_type import SampleType, get_type
from src.samples.plaintext import PlainText

def get_sample(sample_path: str) -> Sample:
    
    type: SampleType = get_type(sample_path)

    if type == SampleType.PLAINTEXT:
        return PlainText(sample_path)

    return None
