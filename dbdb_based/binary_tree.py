# dbdb_based/binary_tree.py
# defines a concrete binary tree algorithm underneath the logical interface.
'''
- BinaryTree provides a concrete implementation of a binary tree, with methods for
  getting, inserting, and deleting key/value pairs. BinaryTree represents an
  immutable tree; updates are performed by returning a new tree which shares
  common structure with the old one.

- BinaryNode implements a node in the binary tree.

- BinaryNodeRef is a specialised ValueRef which knows how to serialise and
  deserialise a BinaryNode.
'''
import pickle
from .logical import LogicalBase
from .logical import ValueRef


class BinaryNode(object):
    def __init__(self, key, value_ref, left_ref=None, right_ref=None, length=1):
        self.key = key
        self.value_ref = value_ref
        self.left_ref = left_ref
        self.right_ref = right_ref
        self.length = length

    def store_refs(self, storage):
        if self.left_ref:
            self.left_ref.store(storage)
        if self.right_ref:
            self.right_ref.store(storage)
        if self.value_ref:
            self.value_ref.store(storage)


class BinaryNodeRef(ValueRef):
    def __init__(self, referent=None, address=None):
        super(BinaryNodeRef, self).__init__(referent, address)

    def prepare_to_store(self, storage):
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_string(referent):
        return pickle.dumps({
            'left': referent.left_ref.address if referent.left_ref else None,
            'key': referent.key,
            'value': referent.value_ref.address if referent.value_ref else None,
            'right': referent.right_ref.address if referent.right_ref else None,
            'length': referent.length,
        })

    @staticmethod
    def string_to_referent(string):
        data = pickle.loads(string)
        return BinaryNode(
            key=data['key'],
            value_ref=ValueRef(address=data['value']),
            left_ref=BinaryNodeRef(address=data['left']) if data['left'] else None,
            right_ref=BinaryNodeRef(address=data['right']) if data['right'] else None,
            length=data['length']
        )


class BinaryTree(LogicalBase):
    node_ref_class = BinaryNodeRef

    def __init__(self, storage):
        super(BinaryTree, self).__init__(storage)

    def set(self, key, value):
        """Insert key, value into the tree."""
        value_ref = ValueRef(referent=value)
        if not self._tree_ref or not self._tree_ref.referent:
            self._tree_ref = self.node_ref_class(
                referent=BinaryNode(key, value_ref)
            )
        else:
            self._tree_ref = self._insert(self._tree_ref, key, value_ref)

    def _insert(self, node_ref, key, value_ref):
        node = node_ref.referent
        if node is None:
            return self.node_ref_class(
                referent=BinaryNode(key, value_ref)
            )

        if key < node.key:
            node.left_ref = self._insert(node.left_ref, key, value_ref) if node.left_ref else self.node_ref_class(
                referent=BinaryNode(key, value_ref)
            )
        elif key > node.key:
            node.right_ref = self._insert(node.right_ref, key, value_ref) if node.right_ref else self.node_ref_class(
                referent=BinaryNode(key, value_ref)
            )
        else:
            node.value_ref = value_ref

        node.length = 1 + (node.left_ref.referent.length if node.left_ref and node.left_ref.referent else 0) + \
                    (node.right_ref.referent.length if node.right_ref and node.right_ref.referent else 0)

        return self.node_ref_class(referent=node)

    def get(self, key):
        """Retrieve a value by key."""
        node_ref = self._tree_ref
        while node_ref and node_ref.referent:
            node = node_ref.referent
            if key < node.key:
                node_ref = node.left_ref
            elif key > node.key:
                node_ref = node.right_ref
            else:
                return node.value_ref.referent
        return None
    
    def commit(self):
        """Persist the current tree to storage."""
        if self._tree_ref:
            # store all refs
            self._tree_ref.store(self._storage)
            # update root address in storage
            self._storage.set_root_address(self._tree_ref.address)
            self._storage.commit()