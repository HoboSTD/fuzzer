"""
Creates a strategy based on the type of file the sample_path is.
"""

from src.samples.sample import Sample
from src.samples.sample_type import SampleType, get_type
from src.strategies.strategy import Strategy
from src.strategies.plaintext import PlainText

def get_strategy(sample_path: str) -> Strategy:

    type: SampleType = get_type(sample_path)

    if type == SampleType.PLAINTEXT:
        strategy = PlainText()
        strategy.set_sample(Sample(sample_path))
        return strategy
