from avl_tree import AVLTreeNode, AVLTree
from unittest import TestCase
import unittest


class TestAVLTree(TestCase):

    # Test Tree should be
    #       28
    #   18        37
    #  8  20    30   67
    def setUp(self):
        juanito = AVLTreeNode(8)
        cami = AVLTreeNode(18)
        vivi = AVLTreeNode(20)
        alejo = AVLTreeNode(28)
        diana = AVLTreeNode(30)
        john = AVLTreeNode(37)
        jairo = AVLTreeNode(67)
        self.test_tree = AVLTree(john)
        self.test_tree.insert(alejo)
        self.test_tree.insert(cami)
        self.test_tree.insert(jairo)
        self.test_tree.insert(diana)
        self.test_tree.insert(vivi)
        self.test_tree.insert(juanito)

    def test_avl_node(self):
        papa = AVLTreeNode(4)
        self.assertEqual(4, papa.node_value)
        self.assertEqual(None, papa.parent)
        self.assertEqual(None, papa.left_child)
        self.assertEqual(None, papa.right_child)

    def test_avl_node_links(self):
        john = AVLTreeNode(37)
        jairo = AVLTreeNode(67)
        juanito = AVLTreeNode(8)
        alejo = AVLTreeNode(28)
        jairo.node_insert(alejo)
        jairo.node_insert(john)
        jairo.node_insert(juanito)
        self.assertEqual(jairo, alejo.parent)
        self.assertEqual(juanito, alejo.left_child)
        self.assertEqual(john, alejo.right_child)
        self.assertEqual(alejo, john.parent)
        self.assertEqual(alejo, juanito.parent)
        self.assertEqual(3, jairo.height())

    def test_left_rotate(self):
        john = AVLTreeNode(37)
        jairo = AVLTreeNode(67)
        alejo = AVLTreeNode(28)
        new_tree = AVLTree(jairo)
        new_tree.insert(john)
        new_tree.insert(alejo)
        self.assertEqual(new_tree.balance, 0)


    def test_balanced_avl(self):
        # Result should be
        #       28
        #   8       67
        # balance = 0
        jairo = AVLTreeNode(67)
        juanito = AVLTreeNode(8)
        alejo = AVLTreeNode(28)
        new_tree = AVLTree(jairo)
        new_tree.insert(alejo)
        new_tree.insert(juanito)
        self.assertEqual(0, new_tree.balance)


    def test_balanced_left_avl(self):
        # Result should be
        #       37
        #   28       67
        #  8
        # balance = -1
        john = AVLTreeNode(37)
        jairo = AVLTreeNode(67)
        juanito = AVLTreeNode(8)
        alejo = AVLTreeNode(28)
        new_tree = AVLTree(john)
        new_tree.insert(alejo)
        new_tree.insert(jairo)
        new_tree.insert(juanito)
        self.assertEqual(-1, new_tree.balance)

    def test_balanced_right_avl(self):
        # Result should be
        #       28
        #   8       67
        #         37
        # balance = 1
        john = AVLTreeNode(37)
        jairo = AVLTreeNode(67)
        juanito = AVLTreeNode(8)
        alejo = AVLTreeNode(28)
        new_tree = AVLTree(alejo)
        new_tree.insert(jairo)
        new_tree.insert(juanito)
        new_tree.insert(john)
        self.assertEqual(1, new_tree.balance)

    def test_balanced_heavy_right_avl(self):
        # insertion is 8 28 37
        # Result should be
        #       28
        #   8       37
        # balance = 0
        john = AVLTreeNode(37)
        juanito = AVLTreeNode(8)
        alejo = AVLTreeNode(28)
        new_tree = AVLTree(juanito)
        new_tree.insert(alejo)
        new_tree.insert(john)
        self.assertEqual(0, new_tree.balance)

    def test_balanced_heavy_left_avl(self):
        # insertion is 37 38 8
        # Result should be
        #       28
        #   8       37
        # balance = 0
        john = AVLTreeNode(37)
        juanito = AVLTreeNode(8)
        alejo = AVLTreeNode(28)
        new_tree = AVLTree(john)
        new_tree.insert(alejo)
        new_tree.insert(juanito)
        self.assertEqual(0, new_tree.balance)

    # Tree should be
    #       28
    #   18        37
    #  8  20    30   67
    def test_find_min_max(self):
        self.assertEqual(8, self.test_tree.parent_node.find_min().node_value)
        self.assertEqual(67, self.test_tree.parent_node.find_max().node_value)

    def test_delete_root(self):
        # Tree result should be
        #       20
        #   18        37
        #  8        30   67
        self.test_tree.delete(28)
        self.assertEqual(AVLTreeNode(20), self.test_tree.parent_node)

    def test_delete_leaf(self):
        # Tree result should be
        #       28
        #   18        37
        #  8        30   67
        self.test_tree.delete(20)
        self.assertEqual(None, self.test_tree.search(20))
        self.assertEqual(3, self.test_tree.parent_node.height())
        self.assertEqual(0, self.test_tree.balance)

    def test_delete_left_child(self):
        # Tree result should be
        #       28
        #   20        37
        #  8        30   67
        self.test_tree.delete(18)
        self.assertEqual(None, self.test_tree.search(18))
        self.assertEqual(3, self.test_tree.parent_node.height())
        self.assertEqual(0, self.test_tree.balance)
        self.assertEqual(20, self.test_tree.parent_node.left_child.node_value)

    def test_delete_right_child(self):
        # Tree result should be
        #       28
        #   18        30
        #  8   20        67
        self.test_tree.delete(37)
        self.assertEqual(None, self.test_tree.search(37))
        self.assertEqual(3, self.test_tree.parent_node.height())
        self.assertEqual(0, self.test_tree.balance)
        self.assertEqual(30, self.test_tree.parent_node.right_child.node_value)


if __name__ == '__main__':
    unittest.main()