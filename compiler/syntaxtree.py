# -*- coding:utf-8 -*-
# __author__ = 'Shanks'


class SyntaxTreeNode(object):

    def __init__(self, value=None, _type=None, extra_info=None):
        self.value = value
        self.type = _type
        self.extra_info = extra_info

        self.father = None
        self.left = None
        self.right = None
        self.first_son = None

    def set_value(self, value):
        self.value = value

    def set_type(self, _type):
        self.type = _type

    def set_extra_info(self, extra_info):
        self.extra_info = extra_info


class SyntaxTree(object):

    def __init__(self):
        self.root = None
        # the dealing node
        self.current = None

    # add a child node and look that if it's father already in the tree
    def add_child_node(self, new_node, father=None):
        if not father:
            father = self.root
        new_node.father = father

        if not father.first_son:
            father.first_son = new_node
        else:
            current_node = father.first_son
            while current_node.right:
                current_node = current_node.right
            current_node.right = new_node
            new_node.left = current_node
        self.current = new_node

    # switch left tree and right tree
    def switch(self, left, right):
        left_left = left.left
        right_right = right.right
        left.left = right
        left.right = right_right
        right.left = left_left
        right.right = left
        if left_left:
            left_left.right = right
        if right_right:
            right_right.left = left

