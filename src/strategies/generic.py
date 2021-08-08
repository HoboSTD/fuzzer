"""
Handles plaintext inputs.
"""

from random import randint
from typing import List
from src.strategies.strategy import Strategy
from src.samples.sample import Sample
from src.strategies.operators import bitflip, byteflip, arithmetic, interestingbytes, bytedelete, randominsert, copyinsert, stretch_at_random
from random import randint

class Generic(Strategy):

    def __init__(self) -> None:
        super().__init__()
        self._state = 0
        self._state_progress = 0
        self._testcase = b''
        self._max_changes = 0

    def get_keywords(self) -> List[bytes]:
        pass

    def set_sample(self, sample: Sample) -> None:
        super().set_sample(sample)
        self._testcase = self._sample._input
        self._lines = self._sample._input.splitlines()

    def get_input(self) -> bytes:
        return self.mutate_machine()

    def reset_testcase(self) -> None:
        self._testcase = self._sample._input
        self._lines = self._sample._input.splitlines()

    def next_state(self) -> None:
        self._state += 1
        self._state_progress = 0
        self._max_changes = 1
        self.reset_testcase()
        print("Generic: New state: ", self._state)
        if self._state >= 19:
            print('Generic: Finished!')

    def mutate_machine(self):
        if self._state == 0:
            if self._state_progress < (len(self._sample._input)*8):
                self._state_progress += 1
                return bitflip(self._testcase, self._state_progress-1)
            else:
                self.next_state()
        if self._state == 1:
            if self._state_progress < (len(self._sample._input)):
                self._state_progress += 1
                return byteflip(self._testcase, self._state_progress-1)
            else:
                self.next_state()
        if self._state == 2:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                return arithmetic(self._testcase)
            else:
                self.next_state()
        if self._state == 3:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                return interestingbytes(self._testcase)
            else:
                self.next_state()
        if self._state == 4:
            if self._state_progress < (len(self._sample._input)):
                self._state_progress += 1
                return bytedelete(self._testcase)
            else:
                self.next_state()
        if self._state == 5:
            if self._state_progress < (len(self._sample._input)):
                self._state_progress += 1
                return randominsert(self._testcase)
            else:
                self.next_state()
        if self._state == 6:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                return copyinsert(self._testcase)
            else:
                self.next_state()
                
        # do everything the same, but this time we build upon the previous test case input
        if self._state == 7:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                self._testcase = byteflip(self._testcase)
                return self._testcase
            else:
                self.next_state()
        if self._state == 8:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                self._testcase = byteflip(self._testcase)
                return self._testcase
            else:
                self.next_state()
        if self._state == 9:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                self._testcase = arithmetic(self._testcase)
                return self._testcase
            else:
                self.next_state()
        if self._state == 10:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                self._testcase = interestingbytes(self._testcase)
                return self._testcase
            else:
                self.next_state()
        if self._state == 11:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                self._testcase = bytedelete(self._testcase)
                return self._testcase
            else:
                self.next_state()
        if self._state == 12:
            if self._state_progress < len(self._sample._input):
                self._state_progress += 1
                self._testcase = randominsert(self._testcase)
                return self._testcase
            else:
                self.next_state()
        if self._state == 13:
            if self._state_progress < len(self._sample._input):
                max_changes = 5
                self._state_progress += 1
                if (self._state_progress % max_changes) == 0:
                    self.reset_testcase()
                
                self._testcase = copyinsert(self._testcase)
                return self._testcase
            else:
                self.next_state()
                
        # take a copy of random line, and insert before or after another random line
        if self._state == 14:
            if self._state_progress < len(self._sample._input):
                max_changes = 50
                self._state_progress += 1
                if (self._state_progress % max_changes) == 0:
                    self.reset_testcase()
                
                src_index = randint(0,  len(self._lines) - 1)
                dest_index = randint(0,  len(self._lines))                
                copy = self._lines[src_index]
                self._lines.insert(dest_index, copy)
                
                return b'\n'.join(self._lines)
            else:
                self.next_state()
                
        # duplicate entire input (all lines)
        if self._state == 15:
            if self._state_progress < 10:
                self._state_progress += 1
                self._lines *= 2
                
                return b'\n'.join(self._lines)
            else:
                self.next_state()
                
        # stretch - max 1 change
        if self._state == 16:
            if self._state_progress < (len(self._sample._input)):
                self._state_progress += 1
                return stretch_at_random(self._testcase)
            else:
                self.next_state()
        # copyinsert with stretch - max 1 change
        if self._state == 17:
            if self._state_progress < (len(self._sample._input)):
                self._state_progress += 1
                return copyinsert(self._testcase, True)
            else:
                self.next_state()
                
        # do everything in random order - 1000 times, max changes between 1-10
        if self._state == 18:
            self._state_progress += 1
            if (self._state_progress % self._max_changes) == 0:
                self._testcase = self._sample._input
                self._max_changes = randint(1, 10)
            if self._state_progress > 1000:
                self.next_state()

            choice = randint(1, 7)
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
            elif choice == 7:
                self._testcase = copyinsert(self._testcase)
	
            return self._testcase

        # We're done
        return None
