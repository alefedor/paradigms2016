from collections.abc import Iterator
from collections import deque


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def set_left(self, child):
        self.left = child
        child.parent = self

    def set_right(self, child):
        self.right = child
        child.parent = self


def insert(tree, item):
    if not tree: return TreeNode(item)
    if tree.value > item: tree.set_left(insert(tree.left, item))
    else: tree.set_right(insert(tree.right, item))
    return tree


def create_tree(items):
    tree = None
    for item in items:
        tree = insert(tree, item)
    return tree


class AbstractTreeIterator(Iterator):
    def __init__(self, root):
        self.root = root
        self.node = root

    @staticmethod
    def left_most(node):
        while node.left:
            node = node.left
        return node

    @staticmethod
    def right_most(node):
        while node.right:
            node = node.right
        return node

    def __next__(self):
        raise NotImplementedError


class InOrder(AbstractTreeIterator):
    def dfs(self, node):
        if node.left:
            for x in self.dfs(node.left):
                yield x
        yield node
        if node.right:
            for x in self.dfs(node.right):
                yield x

    def __init__(self, root):
        super().__init__(root)
        self.iter = self.dfs(self.root)

    def __next__(self):
        return self.iter.__next__().value


class LevelOrder(AbstractTreeIterator):
    def __init__(self, root):
        super().__init__(root)
        self.order = deque()
        self.order.append(root)

    def __next__(self):
        if not self.order:
            raise StopIteration
        a = self.order.popleft()
        if a.left:
            self.order.append(a.left)
        if a.right:
            self.order.append(a.right)
        return a.value


def print_tree(iterator, msg=''):
    print(msg, end=' ')
    for i in iterator:
        print(i, end=' ')
    print()


if __name__ == '__main__':
    tree = create_tree([2, 1, 3, 5, 8, 7])
    #for i in dfs(tree):
    #    print(i.value, end=" ")
    print("")
    print_tree(InOrder(tree), 'In order:')
    print_tree(LevelOrder(tree), 'Level order:')