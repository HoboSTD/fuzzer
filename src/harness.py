"""
Harness the.
"""

from multiprocessing import cpu_count
from threading import Timer
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
        
        # start a timer that kills all the jobs after 179 seconds
        self._timer = Timer(179.0, self.kill_all)
        self._timer.daemon = True
        self._timer.start()

    def kill_all(self):
        """
        Kills all the jobs after a certain amount of seconds have elapsed.
        """

        for job in self._jobs:
            job.kill()
        
        self._jobs.clear()
