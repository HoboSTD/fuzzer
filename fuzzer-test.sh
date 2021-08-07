#!/bin/sh

test_binary() {
    ./fuzzer $1 $1.txt > /dev/null 2>&1
    cat bad.txt | $1 > /dev/null 2>&1

    if [ $? -ne 139 ]; then
        echo "fuzzing "$1" failed"
    else
        echo "fuzzing "$1" passed"
    fi
}

test_binary "binaries/plaintext/plaintext1"
test_binary "binaries/plaintext/plaintext2"
test_binary "binaries/plaintext/plaintext3"
test_binary "binaries/csv/csv1"
test_binary "binaries/csv/csv2"
test_binary "binaries/json/json1"
test_binary "binaries/json/json2"
test_binary "binaries/xml/xml1"
test_binary "binaries/xml/xml2"
