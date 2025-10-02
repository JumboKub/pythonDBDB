# The connect() function opens the database file (possibly creating it, but never overwriting it) and returns an instance of DBDB
from .interface import DBDB
import os

# dbdb/__init__.py
def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return DBDB(f)