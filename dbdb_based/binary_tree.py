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


class BinaryTree(LogicalBase):
    def __init__(self, storage):
        super().__init__()   
        self._storage = storage

    def node_ref_class(self):
        return BinaryNodeRef

    def value_ref_class(self, value=None):
        return ValueRef(value)

    def _get(self, node, key):
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif node.key < key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def _insert(self, node, key, value_ref):
        if node is None:
            new_node = BinaryNode(
                self.node_ref_class(), key, value_ref,
                self.node_ref_class(), 1
            )
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(
                    self._follow(node.left_ref), key, value_ref
                )
            )
        elif node.key < key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(
                    self._follow(node.right_ref), key, value_ref
                )
            )
        else:
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return self.node_ref_class(referent=new_node)


class BinaryNode(object):
    def __init__(self, left_ref, key, value_ref, right_ref, length):
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.length = length

    @staticmethod
    def from_node(node, **kwargs):
        params = {
            'left_ref': node.left_ref,
            'key': node.key,
            'value_ref': node.value_ref,
            'right_ref': node.right_ref,
            'length': node.length,
        }
        params.update(kwargs)
        return BinaryNode(**params)

    def store_refs(self, storage):
        self.value_ref.store(storage)
        self.left_ref.store(storage)
        self.right_ref.store(storage)


class BinaryNodeRef(ValueRef):
    def prepare_to_store(self, storage):
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_string(referent):
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'length': referent.length,
        })
