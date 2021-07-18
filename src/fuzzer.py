"""
The fuzzer.
"""

from src.strategies.strategy import Strategy
from src.strategies.create_strategy import get_strategy
from src.samples.sample import Sample


class Fuzzer():
    
    def __init__(self, sample_path: str) -> None:
        self._sample: Sample = Sample(sample_path)
        self._strategy: Strategy = get_strategy(sample_path)
        self._strategy.set_sample(self._sample)
        self._stop_fuzzing: bool = False

    def fuzz(self) -> bytes:
        """
        Get an input for the fuzzing.
        """

        if self._stop_fuzzing:
            return None
    
        return self._strategy.get_input()

    def analyse(self, returncode: int, input: bytes) -> None:
        """
        Anaylses the output.
        """

        if returncode == -11:
            self._stop_fuzzing = True

            print("Found input that causes segmentation fault.")

            with open("bad.txt", "w") as file:
                file.write(input.decode("utf-8"))
