class RedBlackTreeNode:
    def __init__(self, key, value, color):
        self.key = key
        self.value = value
        self.color = color  # red = true, black = false
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.root = None

    def in_order_traversal(self, node):
        if node is not None:
            yield from self.in_order_traversal(node.left)
            yield node.value
            yield from self.in_order_traversal(node.right)

    def __iter__(self):
        return self.in_order_traversal(self.root)

# insert new node
    def insert(self, key, value):
        new_node = RedBlackTreeNode(key, value, True)  # new is red
        if self.root is None:
            self.root = new_node
            self.root.color = False  # root is black
            return

        # BST insertion
        parent = None
        current = self.root
        while current is not None:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        new_node.parent = parent

        # fix bed - black tree
        self.fix_insert(new_node)

    def fix_insert(self, node):
        # fix after insert
        while node != self.root and node.parent.color:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color:
                    # red uncle
                    node.parent.color = False
                    uncle.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # right child
                        node = node.parent
                        self.left_rotate(node)
                    # left child
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color:
                    node.parent.color = False
                    uncle.color = False
                    node.parent.parent.color = True
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = False
                    node.parent.parent.color = True
                    self.left_rotate(node.parent.parent)
        self.root.color = False



    def left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child


    def right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child



    def find_closest(self, key):
        # find node with closest key in red - black tree
        current = self.root
        closest = None
        closest_diff = float('inf')
        while current:
            diff = abs(current.key - key)
            if diff < closest_diff:
                closest = current
                closest_diff = diff
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return closest.value if closest else None
