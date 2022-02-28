

class AVLTreeNode:
    def __init__(self, value: int):
        self.node_value = value
        self.parent = None
        self.right_child = None
        self.left_child = None

    def __lt__(self, other):
        return self.node_value < (other if type(other) is not AVLTreeNode else other.node_value)

    def __le__(self, other):
        return self.node_value <= (other if type(other) is not AVLTreeNode else other.node_value)

    def __gt__(self, other):
        return self.node_value > (other if type(other) is not AVLTreeNode else other.node_value)

    def __ge__(self, other):
        return self.node_value >= (other if type(other) is not AVLTreeNode else other.node_value)

    def __eq__(self, other):
        return self.node_value == (other if type(other) is not AVLTreeNode else other.node_value)

    def node_insert(self, node):
        if type(node) == AVLTreeNode:
            self.raw_insert(node)

    def raw_insert(self, value):
        if self.node_value > value.node_value if type(value) is AVLTreeNode else value:     # insert to the left
            if self.left_child is None:
                if type(value) == AVLTreeNode:
                    self.left_child = value
                else:
                    self.left_child = AVLTreeNode(value)
                self.left_child.parent = self
            else:
                self.left_child.raw_insert(value)
        if self.node_value < value.node_value if type(value) is AVLTreeNode else value:     # insert to the right
            if self.right_child is None:
                if type(value) == AVLTreeNode:
                    self.right_child = value
                else:
                    self.right_child = AVLTreeNode(value)
                self.right_child.parent = self
            else:
                self.right_child.raw_insert(value)

    def find_min(self):
        if self.left_child is None and self.right_child is None:
            return self
        if self.left_child is None and self.right_child is not None:
            return self.right_child.find_min()
        else:
            return self.left_child.find_min()

    def find_max(self):
        if self.left_child is None and self.right_child is None:
            return self
        if self.right_child is None and self.left_child is not None:
            return self.left_child.find_max()
        else:
            return self.right_child.find_max()

    def search_value(self, value):
        if value == self.node_value:
            return self
        else:
            if value < self.node_value:
                return None if self.left_child is None else self.left_child.search_value(value)
            else:
                return None if self.right_child is None else self.right_child.search_value(value)

    def height(self):
        if self.left_child is None and self.right_child is None:
            return 1

        return 1 + max(0 if self.left_child is None else self.left_child.height(),
                       0 if self.right_child is None else self.right_child.height())


class AVLTree:

    def __init__(self, parent):
        if type(parent) == AVLTreeNode:
            self.parent_node = parent
            self.balance = 0

    def search(self, value):
        return self.parent_node.search_value(value)

    def delete(self, value):
        node_to_delete = self.parent_node.search_value(value)
        if node_to_delete is not None:
            # The node is the root
            if node_to_delete == self.parent_node:
                new_parent = None if node_to_delete.left_child is None else node_to_delete.left_child.find_max()
                papa = new_parent.parent
                papa.right_child = None
                new_parent.parent = None
                new_parent.left_child = node_to_delete.left_child
                new_parent.right_child = node_to_delete.right_child
                if node_to_delete.right_child is not None:
                    node_to_delete.right_child.parent = new_parent.right_child
                # remove children from old root
                node_to_delete.left_child = None
                node_to_delete.right_child = None
                # reference to new root
                self.parent_node = new_parent
            # The node is a leaf
            else:
                if node_to_delete.left_child is None and node_to_delete.right_child is None:
                    papa = node_to_delete.parent
                    node_to_delete.parent = None
                    # remove pointers
                    if papa.left_child == node_to_delete:
                        papa.left_child = None
                    if papa.right_child == node_to_delete:
                        papa.right_child = None
                else:
                    # The node is a right child
                    if node_to_delete > self.parent_node:
                        self._delete_child(node_to_delete, right_direction=True)
                    # The node is a left child
                    if node_to_delete < self.parent_node:
                        self._delete_child(node_to_delete, right_direction=False)
        # finally, validate the AVL balance condition
        self._check_avl_balance()

    def _check_avl_balance(self):
        # balance maintenance
        self.balance = (0 if self.parent_node.right_child is None else self.parent_node.right_child.height()) \
                       - (0 if self.parent_node.left_child is None else self.parent_node.left_child.height())
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1: # perform a left rotation
                self.parent_node = self.left_rotate()
            if self.balance < -1: # perform a right rotation
                self.parent_node = self.right_rotate()
            # balance maintenance
            self.balance = (0 if self.parent_node.right_child is None else self.parent_node.right_child.height()) \
                           - (0 if self.parent_node.left_child is None else self.parent_node.left_child.height())

    def _delete_child(self, node_to_delete, right_direction: bool):
        # find the new right child
        new_sub_tree = node_to_delete.find_min()
        if not right_direction:  # Deleting a child on the left
            new_sub_tree = node_to_delete.find_max()
        if new_sub_tree != node_to_delete:
            # remove the links from node to delete
            papa = node_to_delete.parent
            new_right_tree_children = node_to_delete.right_child
            new_left_tree_children = node_to_delete.left_child
            if not right_direction:
                new_right_tree_children = None
            else:
                new_left_tree_children = None

            node_to_delete.parent = None
            node_to_delete.right_child = None
            node_to_delete.left_child = None
            # Update papa
            if right_direction:
                papa.right_child = None
            else:
                papa.left_child = None
            new_sub_tree.parent = papa

            if right_direction:
                papa.right_child = new_sub_tree
            else:
                papa.left_child = new_sub_tree

            # and reasign chilren to the left
            if new_left_tree_children is not None:
                new_left_tree_children.parent = new_sub_tree
            new_sub_tree.left_child = new_left_tree_children
            # and reasign chilren to the right
            if new_right_tree_children is not None:
                new_right_tree_children.parent = new_sub_tree
            new_sub_tree.right_child = new_right_tree_children
        else:
            papa = node_to_delete.parent
            node_to_delete.parent = None
            if papa is not None:
                if node_to_delete > papa:
                    papa.right_child = None
                else:
                    papa.left_child = None

    ## balanced node insertion
    def insert(self, value):
        node = value
        if type(value) != AVLTreeNode:
            node = AVLTreeNode(value)
        self.parent_node.node_insert(node)
        self._check_avl_balance()


    # Rotates the left child to be the parent of the current node, which will become the new right child.
    # The right child of the new parent becomes the left child of the new right child.
    def right_rotate(self):
        new_parent = self.parent_node
        if self.parent_node.left_child is not None:
            new_parent = self.parent_node.left_child
            new_child = self.parent_node
            new_child.parent = new_parent
            new_parent.parent = None
            new_child.left_child = None
            # new_parent.right_child
            if new_parent.right_child is not None:
                new_child.left_child = new_parent.right_child
                if new_parent.right_child is not None:
                    new_parent.right_child.parent = new_child
                new_parent.right_child = None
            new_parent.right_child = new_child
        return new_parent

    # Rotates the right child to be the parent of the current node,
    #   which will become the new left child.
    def left_rotate(self):
        new_parent = self.parent_node
        if self.parent_node.right_child is not None:
            new_parent = self.parent_node.right_child
            new_child = self.parent_node
            new_child.parent = new_parent
            new_parent.parent = None
            new_child.right_child = None
            # new_parent.right_child
            if new_parent.left_child is not None:
                new_child.right_child = new_parent.left_child
                if new_parent.left_child is not None:
                    new_parent.left_child.parent = new_child
                new_parent.left_child = None
            new_parent.left_child = new_child
        return new_parent
