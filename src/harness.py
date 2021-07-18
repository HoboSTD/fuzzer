"""
Harness the.
"""

from src.jobs.job import Job
from src.fuzzer import Fuzzer

class Harness():
    """
    Does stuff.
    """
    
    def __init__(self, binary_path: str, sample_path: str) -> None:
        self._binary_path = binary_path
        self._fuzzer = Fuzzer(sample_path)

    def start(self):
        """
        Creates a job and then makes it start fuzzing.
        """
        
        job = Job(self._fuzzer, self._binary_path)
        job.start()
