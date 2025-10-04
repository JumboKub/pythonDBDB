# defines the logical layer. It's an abstract interface to a key/value store.
'''
-LogicalBase provides the API for logical updates (like get, set, and commit) and defers to a concrete subclass to implement the updates themselves. It also manages storage locking and dereferencing internal nodes.

-ValueRef is a Python object that refers to a binary blob stored in the database. The indirection lets us avoid loading the entire data store into memory all at once.
'''
import pickle

# dbdb/logical.py
class ValueRef(object):
    """
    A reference to a value stored in the storage system.
    It may hold either a referent (the actual Python object) or an address (on-disk pointer).
    """

    def __init__(self, referent=None, address=None):
        self._referent = referent
        self._address = address

    @property
    def referent(self):
        return self._referent

    @property
    def address(self):
        return self._address

    def prepare_to_store(self, storage):
        """Override in subclasses to prepare internal references for storage."""
        pass

    def store(self, storage):
        """
        Write the referent to storage and record its address.
        """
        if self._referent is not None and self._address is None:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))

    @staticmethod
    def referent_to_string(referent):
        """Convert referent into a storable string (override in subclass)."""
        return pickle.dumps(referent)

    @staticmethod
    def string_to_referent(string):
        """Rebuild referent from stored string (override in subclass)."""
        return pickle.loads(string)


class LogicalBase(object):
    """
    Base for logical structures like BinaryTree.
    Handles root reference and interaction with storage.
    """

    def __init__(self, storage):
        self._storage = storage
        self._tree_ref = self.node_ref_class(address=self._storage.get_root_address())

    @property
    def root(self):
        return self._tree_ref

    def store(self):
        """
        Store root reference into storage.
        """
        if self._tree_ref:
            self._tree_ref.store(self._storage)
            self._storage.set_root_address(self._tree_ref.address)