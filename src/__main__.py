from src.utils import *
from src.fuzz_csv import *
from src.fuzz_json import *
from src.thread import Thread
from src.path import check_path_exists
from sys import argv

if len(argv) != 3:
    print("Usage: ./fuzzer binary binaryinput")
else:
    binary_path = check_path_exists(argv[1])
    sample_path = check_path_exists(argv[2])

    with open(sample_path) as file:
        if is_csv(file):
            fuzzer = fuzz_csv(file)
        elif is_json(file):
            fuzzer = fuzz_json(file)
    Thread.get_instance().init_thread(fuzzer)