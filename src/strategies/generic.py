"""
Handles plaintext inputs.
"""

from typing import List
from src.strategies.strategy import Strategy
from src.samples.sample import Sample
from src.strategies.operators import bitflip, byteflip, arithmetic, interestingbytes, bytedelete, randominsert
from random import randint

class Generic(Strategy):

    def __init__(self) -> None:
        super().__init__()
        self._state = 0
        self._state_progress = 0

    def get_keywords(self) -> List[bytes]:
        pass

    def set_sample(self, sample: Sample) -> None:
        super().set_sample(sample)
        self._testcase = self._sample._input

    def get_input(self) -> bytes:
        return self.mutate_machine()

    def next_state(self) -> None:
        self._state += 1
        self._state_progress = 0

    def mutate_machine(self):
        if self._state == 0:
            if self._state_progress < len(self._testcase):
                self._state_progress += 1
                return bitflip(self._testcase)
            else:
                self.next_state()
        elif self._state == 1:
            if self._state_progress < len(self._testcase):
                self._state_progress += 1
                return byteflip(self._testcase)
            else:
                self.next_state()
        elif self._state == 2:
            if self._state_progress < len(self._testcase):
                self._state_progress += 1
                return arithmetic(self._testcase)
            else:
                self.next_state()
        elif self._state == 3:
            if self._state_progress < len(self._testcase):
                self._state_progress += 1
                return interestingbytes(self._testcase)
            else:
                self.next_state()
        elif self._state == 4:
            if self._state_progress < len(self._testcase):
                self._state_progress += 1
                return bytedelete(self._testcase)
            else:
                self.next_state()
        elif self._state == 5:
            if self._state_progress < len(self._testcase):
                self._state_progress += 1
                return randominsert(self._testcase)
            else:
                self.next_state()
        elif self._state == 6:
            choice = randint(1, 6)
            if choice == 1:
                self._testcase = bitflip(self._testcase)
            elif choice == 2:
                self._testcase = byteflip(self._testcase)
            elif choice == 3:
                self._testcase = arithmetic(self._testcase)
            elif choice == 4:
                self._testcase = interestingbytes(self._testcase)
            elif choice == 5:
                self._testcase = bytedelete(self._testcase)
            elif choice == 6:
                self._testcase = randominsert(self._testcase)

            return self._testcase

        return None