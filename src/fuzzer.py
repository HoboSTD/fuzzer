"""
The fuzzer.
"""

from time import time
from src.strategies.generic import Generic
from typing import List
from src.strategies.strategy import Strategy
from src.strategies.create_strategy import get_strategy
from src.samples.sample import Sample


class Fuzzer():
    
    def __init__(self, sample_path: str) -> None:
        self._sample: Sample = Sample(sample_path)
        self._strategy: Strategy = get_strategy(sample_path)
        self._strategy.set_sample(self._sample)
        self._stop_fuzzing: bool = False
        self._generic: Generic = Generic()
        self._generic.set_sample(self._sample)
        self.ninputs: int = 0
        self.reports: List[Report] = [
            Report("success"),
            Report("hang"),
            Report("exit()"),
            Report("abort()"),
            Report("other")]
        self.start: float = time()
        self.last_report: float = time()

    def fuzz(self) -> bytes:
        """
        Get an input for the fuzzing.
        """

        if self._stop_fuzzing:
            return None

        input = self._generic.get_input()
        if input != None:
            return input
    
        return self._strategy.get_input()

    def print_reports(self):
        for report in self.reports:
            print(report.message())
    
    def print_inputs_a_sec(self):
        
        try:
            inputs_sec = self.ninputs / (time() - self.start)
            print(f"{inputs_sec:.2f} inputs/sec")
        except:
            pass
    
    def report(self, time_between = 2):

        if time() - self.last_report < time_between:
            return

        print("-"*80)
        self.print_inputs_a_sec()
        self.print_reports()
        print("-"*80)
        print()
        self.last_report = time()

    def analyse(self, returncode: int, input: bytes) -> None:
        """
        Anaylses the output.
        """

        self.ninputs += 1
        self.report()

        if returncode == 0:
            self.reports[0].inc_count()
        elif returncode == 124:
            self.reports[1].inc_count()
        elif returncode > 0:
            self.reports[2].inc_count()
        elif returncode == -6:
            self.reports[3].inc_count()
        elif returncode == -11:
            self._stop_fuzzing = True

            self.report(-1)

            print("Found input that causes segmentation fault.")

            with open("bad.txt", "wb") as file:
                file.write(input)
        else:
            self.reports[4].inc_count()

class Report():
    
    def __init__(self, code: str) -> None:
        self.count = 0
        self.code = code

    def inc_count(self):
        self.count += 1
    
    def message(self):
        return f"Error type: {self.code} has happened {self.count} times."
