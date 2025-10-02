# defines a class (DBDB) which implements the Python dictionary API using the concrete BinaryTree implementation. This is how you'd use DBDB inside a Python program.
from .binary_tree import BinaryTree
from .storage import Storage

print("Storage is being imported from:", Storage.__module__, Storage)
# dbdb/interface.py
class DBDB(object):

    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def __getitem__(self, key):
        self._assert_not_closed()
        return self._tree.get(key)

    def _assert_not_closed(self):
        if self._storage.closed:
            raise ValueError('Database closed.')
        
    def __setitem__(self, key, value):
        self._assert_not_closed()
        return self._tree.set(key, value)
    def commit(self):
        self._assert_not_closed()
        self._tree.commit()
