import portalocker

# dbdb/storage.py
class Storage(object):
    def __init__(self, f):
        self._f = f
    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False