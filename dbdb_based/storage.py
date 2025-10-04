import portalocker
import os

class Storage(object):
    def __init__(self, f):
        self._f = f
        self.locked = False
        self.closed = False
        self._root_address = None

        # If file is empty, initialize superblock
        self._f.seek(0, os.SEEK_END)
        if self._f.tell() == 0:
            # reserve 8 bytes for root address
            self._f.write(b"\x00" * 8)
            self._f.flush()
        else:
            # read existing root address
            self._f.seek(0)
            raw = self._f.read(8)
            if raw:
                self._root_address = int.from_bytes(raw, "big")

    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
        return True

    def unlock(self):
        if self.locked:
            portalocker.unlock(self._f)
            self.locked = False

    def close(self):
        if not self.closed:
            self._f.close()
            self.closed = True

    # --- Persistence methods ---

    def write(self, data: bytes) -> int:
        """Append data to file, return its address (offset)."""
        self._f.seek(0, os.SEEK_END)
        address = self._f.tell()
        self._f.write(len(data).to_bytes(4, "big"))  # length prefix
        self._f.write(data)
        self._f.flush()
        return address

    def read(self, address: int) -> bytes:
        """Read data back from an address."""
        self._f.seek(address)
        size = int.from_bytes(self._f.read(4), "big")
        return self._f.read(size)

    def set_root_address(self, address: int):
        self._root_address = address

    def get_root_address(self) -> int:
        return self._root_address

    def commit(self):
        """Flush root address and unlock."""
        if self._root_address is not None:
            self._f.seek(0)
            self._f.write(self._root_address.to_bytes(8, "big"))
            self._f.flush()
        self.unlock()
