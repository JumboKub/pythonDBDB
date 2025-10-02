# defines the logical layer. It's an abstract interface to a key/value store.
'''
-LogicalBase provides the API for logical updates (like get, set, and commit) and defers to a concrete subclass to implement the updates themselves. It also manages storage locking and dereferencing internal nodes.

-ValueRef is a Python object that refers to a binary blob stored in the database. The indirection lets us avoid loading the entire data store into memory all at once.
'''

# dbdb/logical.py
class LogicalBase(object):
# ...
    def get(self, key):
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)
    
    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(
            address=self._storage.get_root_address())
        
    def set(self, key, value):
        if self._storage.lock():
            self._refresh_tree_ref()
        self._tree_ref = self._insert(
            self._follow(self._tree_ref), key, self.value_ref_class(value))
        
    def commit(self):
        self._tree_ref.store(self._storage)
        self._storage.commit_root_address(self._tree_ref.address)

class ValueRef(object):
# ...
    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))