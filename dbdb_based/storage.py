import portalocker

# dbdb/storage.py
class Storage(object):
    def __init__(self, f):
        self._f = f
        self.closed = False
        self.locked = False
        self._root_address = None

    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        return False

    def unlock(self):
        if self.locked:
            self.locked = False
            return True
        return False
    
    def close(self):
        self._f.close()
        self.closed = True

    def get_root_address(self):
        return self._root_address
    
    def commit_root_address(self, root_address):
        self._root_address = root_address
        self._f.flush()