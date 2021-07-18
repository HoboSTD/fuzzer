"""
Creates a strategy based on the type of file the sample_path is.
"""

from src.samples.sample import Sample
from src.samples.sample_type import SampleType, get_type
from src.strategies.strategy import Strategy
from src.strategies.plaintext import PlainText
from src.strategies.csv import Csv
from src.strategies.json import JsonStrategy

def get_strategy(sample_path: str) -> Strategy:

    type: SampleType = get_type(sample_path)
    sample: Sample = Sample(sample_path)

    if type == SampleType.CSV:
        strategy = Csv()
        strategy.set_sample(sample)
        return strategy
    elif type == SampleType.JSON:
        strategy = JsonStrategy()
        strategy.set_sample(sample)
        return strategy
    else:
        strategy = PlainText()
        strategy.set_sample(sample)
        return strategy
