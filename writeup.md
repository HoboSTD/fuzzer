# Fuzzer Functionality

The fuzzer takes in a binary and a text file. It is able to detect all file types.
It can fuzz plaintext, csv and json formats and performs mutations based on the file type.
Generally, it detects memory corruption bugs by looking for segmentation faults that would be
indicated by the exit code after a sent mutated input. The mutations used are: overflows, format
strings, bitflipping…
After detecting a segmentation fault, a file called “bad.txt” will be created that will contain the
input that caused the segmentation fault along with the exit code.

# Fuzzer Design

The fuzzer uses strategies based on the detected file type to mutate the input. A job takes the
input from the fuzzer and runs the binary with this input. It then gives the input along with the
return code back to the fuzzer. If the input results in a segmentation fault then the fuzzer is
stopped and the input is saved. The harness creates and starts this job.
The harness only executes a single job at a time.
The fuzzer can only fuzz json, csv and plaintext files. The fuzzer can be improved by adding
functionality to fuzz more file types such as PDFs, XMLs and so on.
It can fuzz csv2 as well.
