"""
Used to test what the values of returncodes.
"""

import pytest
from src.jobs.job import Job

@pytest.mark.parametrize("path,returncode", [
    ("binaries/test/abort", -6),
    ("binaries/test/exit-status", 1),
    ("binaries/test/segfault", -11),
    ("binaries/test/normal", 0),
    ("binaries/test/hang", 124),
])
def test_exitcode(path: str, returncode: int):
    job = Job(None, path)
    assert job.execute(b"") == returncode
