from pwn import *
import csv
import json

# https://docs.python.org/3/library/csv.html
def is_csv(file):
    try:
        dialect = csv.Sniffer().sniff(file.read(1024))
        file.seek(0)
    except csv.Error:
        return False
    
    excel_delimiter = csv.excel.delimiter
    excel_tab_delimiter = csv.excel_tab.delimiter
    file_delimiter = dialect.delimiter
    
    if ((excel_delimiter == file_delimiter) or (excel_tab_delimiter == file_delimiter)):
        return True
    else:
        return False

# https://docs.python.org/3/library/json.html
def is_json(file):
    try:
        json_object = json.load(file)
        file.seek(0)
    except ValueError:
        return False
    
    return True

