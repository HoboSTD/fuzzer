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

# Documentation

## How the fuzzer works

The fuzzer first determines the file type and then selects a strategy based on the file type. If
no file type can be determined, then the plaintext strategy is chosen as the format-specific strategy. It then runs the generic fuzzing strategy against the input, and then uses the format-specific fuzzing strategy that was selected. 

Jobs take an input from the fuzzer by calling `fuzzer.fuzz()`. They then execute the binary using
this input. The job then calls `fuzzer.analyse(returncode, input)` after the binary is executed.

The fuzzer checks the returncode to determine what caused the crash: either it returned 0 and so was
successful, returned 124 which means the program hung, returned something greater than 0 which means
the program exited or returned -6 which means the program aborted.

### Parameters

These parameters are used to generate fuzzed values based on their type. This makes it easier to
generate fuzzed values in each strategy.

#### Integer

This generates random integers in the range [-2^30, 2^30].

#### String

This either returns the original value or returns a string with a bunch of "%s"s. This attempts to
find format string or buffer overflow vulnerabilities.

#### List

This returns a list of parameters. Each of these parameters is either an integer, string or list.
They are fuzzed each time the list is fuzzed.

### Generic Fuzzing Strategy

The "Generic" strategy is used against all input formats prior to their format-specific strategies.
This is because the strategy uses a set of common operations that don't rely on the input being of a specific format e.g. JSON, XML.

Operations which are included in the fuzzing process:
 - Bit flip - inverts n consecutive bits.
 - Byte flip - inverts n consecutive bytes.
 - Arithmetic - performs addition and subtraction on n consecutive bytes..
 - Interesting bytes - randomly replaces n consecutive bytes with interesting values e.g. 0, 0xFF, 0x7F.
 - Byte delete - randomly deletes n consecutive bytes.
 - Random insert - insert n consecutive random bytes, at a random location.
 - Copy insert - copies 1-n consecutive bytes from a random location, and inserts at another random location.
 - Stretch - selects a random location and stretches 1-n bytes there, to a certain length.

### Plaintext Fuzzing Strategy

The plaintext strategy splits the sample input into lines and then creates a parameter based on the
line's type.

Each generated input combines all the fuzzed parameters (joined with new lines).

### JSON Fuzzing Strategy

This strategy mainly focuses on manipulating the JSON structures such as keys and values.
It does not attempt to fuzz any syntactical related bugs.

The current JSON fuzzing process is as follows:

1. 
    - Change every value in the JSON object to a very large string - buffer overflow vulnerabilities.
    - Change every value to a large string containing "%s" - fmt string vulnerabilities.
2.
    - For every value of string type, append interesting bytes on each iteration.
    - For every value of integer type, double the number and change the sign on each iteration.
    - For every value of list type, do the above for every element in that list, and also append more elements.
    - Stop this process when each value gets very large.
3.
    - Add new key-value pairs to the root of the JSON - values are strings and integers.
4.
    - Recursively mutate the entire JSON object with random values.
    - Do this indefinitely.

### CSV Fuzzing Strategy

The csv strategy converts the sample input into a 2d array where each cell is a parameter.

Each generated input combines all the fuzzed cells into a valid csv format. This is so that the
generic strategy can perform operatings like bit-flipping to mess with the csv structure.

### XML Fuzzing Strategy

The xml strategy converts the sample input into a tree where each node has a tag, a list of
attributes and a list of children.

Each generated input messes with the xml in the following way:

- changing the tag name.
- not including an opening tag.
- massively increasing the number of attributes.
- fuzzing the attribute structure.
- fuzzing the attribute's name or value.
- not including child nodes.
- massively increasing the number of child nodes.
- including fuzzed string for the node's content.
- generating lots of nested tags.
- not including a closing tag.

This means that the structure and values of the xml are all fuzzed.

### JPG Fuzzing Strategy

### Harness

The harness creates a list of jobs that each exist in their own thread. These jobs take input from
the fuzzer and test it against the binary. The return code of the program is then given back to the
fuzzer, along with the input that caused it.

Each job lets the binary execute for 5 seconds before it is killed, this is a heuristic we use to detect if the program is stuck in an infinite loop.

After 180 seconds the harness kills all the jobs.

## What bugs can be found

The fuzzer has found buffer overflow vulnerabilities and format string vulnerabilities, but it may also be possible to find other vulns i.e. heap based.

## Future Improvements

### Code Coverage and Coverage based mutations

The fuzzer does not analyse the code coverage of the program. Because of this it can't do coverage
based mutation either.

### Avoiding overheads

The fuzzer doesn't create extra files but it still uses `execve()` to run the binary.

Our approach to in memory resetting was going to be forking the process before it received input.

### ELF and PDF, and more

The fuzzer doesn't understand ELF, PDF, etc formats.

### Segfault input compression

Sometimes the input we have used to crash the program is quite complex and large, this can be quite troublesome when it comes to actually fixing the vulnerability, as it is unclear which part of the input caused the crash.
Using a bruteforce technique, it may be trivial to compress the input, whilst still retaining the property that causes the crash.
Once then input can't be reduced any futher, we save this instead as it's easier to debug.

## Something Awesome
