from problem1 import *
from problem2 import *
import numpy as np

'''
    Unit test 1:
    This file includes unit tests for problem1.py.
    You could test the correctness of your code by typing `nosetests -v test1.py` in the terminal.
'''
grammar_path = '../data/grammar.gr'
cfg = CFG()
cfg.load_grammar(grammar_path)
# set randomness to False for testing purpose
# to generate interesting sentences, set randomness = True
gen = Generator(cfg, False)

def test_selectRule():
    ''' (15 points) problem2: selectRule'''
    for lhs in cfg.lhs2rhs.keys():
        rhss = [rhs for rhs, count in cfg.lhs2rhs[lhs]]
        rhs = gen.select_rule(lhs)
        assert rhs in rhss

def test_grow_and_print_node():
    ''' (20 points) problem2: grow_node and print_node'''
    root = Node('ROOT')
    gen.grow_node(root)
    assert gen.print_node(root) == '(ROOT (S (NP (Det a) (Noun pickle)) (VP (Verb wanted) (NP (Det a) (Noun pickle)))) .)'