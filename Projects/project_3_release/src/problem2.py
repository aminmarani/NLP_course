import random
from problem1 import *

class Node:
    def __init__(self, _symbol):
        self.symbol = _symbol
        self.leftChild = None
        self.rightChild = None

class Generator:
    def __init__(self, _cfg:CFG, randomness):
        self.cfg = _cfg
        self.random_selection = randomness

    def generate_sentences(self, numSentences):
        for i in range(numSentences):
            root = Node('ROOT')
            self.grow_node(root)
            print(self.print_node(root))

    def grow_node(self, node:Node):
        """
        Expand one node by calling the function select_rule to pick one rule for the expansion.
        :param node: the node to be expanded
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    def print_node(self, node:Node):
        """
        Recursively print the tree rooted at node.
        :param node: the node to be expanded
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    def select_rule(self, lhs):
        """
        select a rule with the given lhs.
        :param lhs: the given lhs. Random selection using the rule probabilities if self.random_selection = True
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################