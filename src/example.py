"""
An example of how the files are layed out.
"""

def read_file(filename: str) -> str:
    """
    Returns the content of the file with the filename.
    """

    contents = []
    with open(filename, "r") as file:
        for line in file.readlines():
            contents.append(line.strip("\n"))

    return '\n'.join(contents)
