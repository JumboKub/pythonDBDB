# dbdb_based/__init__.py
import os
from .interface import DBDB

def connect(filename):
    """Open a database file and return a DBDB object."""
    if os.path.exists(filename):
        f = open(filename, "r+b")
    else:
        f = open(filename, "w+b")

    return DBDB(f)
