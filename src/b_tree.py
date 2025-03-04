class BTreeNode:
    # initialize b - tree node
    def __init__(self, leaf=False):
        self.keys = []  # (key, value) pairs
        self.children = []
        self.leaf = leaf  # true if  node is a leaf


class BTree:
    # initialize the b - tree
    def __init__(self, order=4):
        self.order = order # tree degree
        self.root = BTreeNode(leaf=True) # empty leaf to begin

    def traverse(self, node):
        # in order traversal for the b - tree
        if node is not None:
            for i in range(len(node.keys)):
                # visit left child before key
                if len(node.children) > 0:
                    yield from self.traverse(node.children[i])
                # yield current key value
                yield node.keys[i][1]
            # visit the right most child node
            if len(node.children) > 0:
                yield from self.traverse(node.children[-1])

    def __iter__(self):
        return self.traverse(self.root)

    def insert(self, key, value):
        # insert new key and value pair in the b - tree
        root = self.root
        # split if root is full
        if len(root.keys) == (2 * self.order) - 1:
            new_node = BTreeNode(leaf=False) # new becomes non leaf
            self.root = new_node
            new_node.children.append(root) # old becomes child
            self.split_child(new_node, 0)
            self.insert_non_full(new_node, key, value)
        else:
            self.insert_non_full(root, key, value)

    def insert_non_full(self, node, key, value):
        # insert key to an available node
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append((None, None))  # temp
            while i >= 0 and key < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = (key, value)
        else:
            while i >= 0 and key < node.keys[i][0]:
                i -= 1
            i += 1
            # split if child is full
            if len(node.children[i].keys) == (2 * self.order) - 1:
                self.split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            self.insert_non_full(node.children[i], key, value)

    def split_child(self, parent, index):
        # split child into 2 nodes
        full_node = parent.children[index]
        mid = self.order - 1 # mid point

        # new node right of the mid point
        new_node = BTreeNode(leaf=full_node.leaf)
        parent.keys.insert(index, full_node.keys[mid])
        parent.children.insert(index + 1, new_node)

        # split between the 2 nodes
        new_node.keys = full_node.keys[mid + 1:]
        full_node.keys = full_node.keys[:mid]

        if not full_node.leaf:
            new_node.children = full_node.children[mid + 1:]
            full_node.children = full_node.children[:mid + 1]

    def find_closest(self, key):
        # find the key and value pair w closest key
        def closest_in_node(node, key):
            closest_pair = None
            closest_diff = float('inf')
            for i, (k, v) in enumerate(node.keys):
                diff = abs(k - key)
                if diff < closest_diff:
                    closest_pair = (k, v)
                    closest_diff = diff
            return closest_pair

        current = self.root
        closest_pair = None
        while current:
            closest_pair = closest_in_node(current, key)
            if not current.leaf:
                for i, (k, _) in enumerate(current.keys):
                    if key < k:
                        current = current.children[i]
                        break
                else:
                    current = current.children[-1]
            else:
                break
        return closest_pair[1] if closest_pair else None
