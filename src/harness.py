"""
Harness the.
"""

from multiprocessing import cpu_count
from typing import List
from src.jobs.job import Job
from src.fuzzer import Fuzzer

class Harness():
    """
    Does stuff.
    """
    
    def __init__(self, binary_path: str, sample_path: str) -> None:
        self._binary_path = binary_path
        self._fuzzer = Fuzzer(sample_path)
        self._njobs = cpu_count() - 1
        self._jobs: List[Job] = []

    def start(self):
        """
        Creates njobs and then makes it start fuzzing.
        """

        for _ in range(0, self._njobs):
            job = Job(self._fuzzer, self._binary_path)
            job.start()
            self._jobs.append(job)
