# 1. The aim of this script is to calculate 24 given any 4 intergers
# 2. The idea is to construct random bifurcaed trees to search for tree with
#    a root node of 24
# 3. Inspired by 强哥 from[https://zhuanlan.zhihu.com/p/37608401]
import math
import itertools
import re

class Node(object):
    def __init__(self, result=None):
        self._left = None
        self._right = None
        self._operator = None
        self._result = result

    def set_expression(self, left_node, right_node, operator):
        self._left = left_node
        self._right = right_node
        self._operator = operator
        expression = "{} {} {}".format(left_node._result, operator, right_node._result)
        self._result = eval(expression)

    def __repr__(self):
        if self._operator:
            return '<Node equation="{} {} {}", result="{}">'.format(self._left._result, self._operator, self._right._result, self._result)
        else:
            return '<Node value="{}">'.format(self._result)

    def get_expression(self):
        if self._operator:
            return self._operator


def build_all_trees(array):
    if len(array) == 1:
        tree = Node(array[0])
        return [tree]

    treelist = []
    for i in range(1, len(array)):
        left_array = array[:i]
        right_array = array[i:]
        left_trees = build_all_trees(left_array)
        right_trees = build_all_trees(right_array)
        for left_tree in left_trees:
            for right_tree in right_trees:
                combined_trees = build_tree(left_tree, right_tree)
                treelist.extend(combined_trees)
    return treelist


def build_tree(left_tree, right_tree):
    treelist = []
    tree1 = Node()
    tree1.set_expression(left_tree, right_tree, "+")
    treelist.append(tree1)
    tree2 = Node()
    tree2.set_expression(left_tree, right_tree, "-")
    treelist.append(tree2)
    tree4 = Node()
    tree4.set_expression(left_tree, right_tree, "*")
    treelist.append(tree4)
    if right_tree._result != 0:
        tree5 = Node()
        tree5.set_expression(left_tree, right_tree, "/")
        if((tree5._result).is_integer()):
            treelist.append(tree5)
    return treelist


def get_equation(tree):
    if(tree._operator is None):
        return tree._result
    elif(tree._left._operator is None and tree._right._operator is None):
        return "({0} {1} {2})".format(tree._left._result, tree._operator, tree._right._result)

    equation = ""
    if(tree._left is not None or tree._right is not None):
        L = get_equation(tree._left)
        R = get_equation(tree._right)
        equation = "({0} {1} {2})".format(L, tree._operator, R)
    return equation


def find_24(array):
    perms = itertools.permutations(array)
    found = False
    for perm in perms:
        treelist = build_all_trees(perm)
        for tree in treelist:
            if math.isclose(tree._result, 24, rel_tol=1e-10):
                expression = get_equation(tree)
                print("===================================")
                print("We found a solution:")
                print("{} - {}".format(perm, expression))
                found = True
                break
        if found:
            break
    if(found is False):
        print("Sorry I can not work out a solution.")


if __name__ == "__main__":
    print("Welcome!")
    integers = input("Please key in your 4 intergers.(Please separate them with space.)")
    intList = integers.split()
    print("Your input integers are: {}".format(intList))
    find_24(intList)
