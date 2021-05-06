import random
from problem1 import *
import numpy as np

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
        out = self.select_rule(node.symbol)
        if out != None: #expand the node
            out = out.split(' ') #some rhs are 2 non-terminals and some are 1 terminals
            node.leftChild = Node(out[0])
            self.grow_node(node.leftChild)
            if len(out) == 2: #there is another child to expand
                node.rightChild = Node(out[1])
                self.grow_node(node.rightChild)
        #########################################

    def print_node(self, node:Node):
        """
        Recursively print the tree rooted at node.
        :param node: the node to be expanded
        """
        #########################################
        if node.leftChild != None and node.rightChild != None:
            s = '(' + node.symbol
        #print(node.symbol)
        #if node.leftChild != None:
            s+= ' '+ self.print_node(node.leftChild)
        #if node.rightChild != None:
            s+= ' ' + self.print_node(node.rightChild)

            s += ')'

            return s
        else:
            return '(' + node.symbol + ' ' + node.leftChild.symbol + ')'

        #########################################

    def select_rule(self, lhs):
        """
        select a rule with the given lhs.
        :param lhs: the given lhs. Random selection using the rule probabilities if self.random_selection = True
        """
        #########################################
        rnd = np.random.rand()

        #return None #if the lhs does not exist
        if lhs not in self.cfg.lhs2rhs.keys():
            return None

        if not self.random_selection : #return the top one
            return self.cfg.lhs2rhs[lhs][0][0]
        s = 0 #sum of random numbers
        for items in self.cfg.lhs2rhs[lhs]:
            s += items[1]
            if rnd <= s:
                return items[0]
        
        #########################################



# grammar_path = '../data/grammar.gr'
# cfg = CFG()
# cfg.load_grammar(grammar_path)
# # set randomness to False for testing purpose
# # to generate interesting sentences, set randomness = True
# gen = Generator(cfg, False)

# for lhs in cfg.lhs2rhs.keys():
#     rhss = [rhs for rhs, count in cfg.lhs2rhs[lhs]]
#     rhs = gen.select_rule(lhs)

# root = Node('ROOT')
# gen.grow_node(root)
# print(gen.print_node(root))