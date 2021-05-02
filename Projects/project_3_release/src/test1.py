from problem1 import *
import numpy as np

'''
    Unit test 1:
    This file includes unit tests for problem1.py.
    You could test the correctness of your code by typing `nosetests -v test1.py` in the terminal.
'''
grammar_path = '../data/grammar.gr'
cfg = CFG()
cfg.load_grammar(grammar_path)

# -------------------------------------------------------------------------
def test_symbol_type():
    ''' (5 points) problem1: symbol_type'''
    assert cfg.symbol_type('Verb') == 1, 'fail test of Verb'
    assert cfg.symbol_type('S') == 2, 'fail test of S'
    assert cfg.symbol_type('ate') == 0, 'fail test of ate'

# -------------------------------------------------------------------------
def test_load_grammar():
    ''' (15 points) problem1: load_grammar'''    
    assert len(cfg.terminals) == 22, 'there are 22 terminals'
    assert len(cfg.non_terminals) == 5, 'there are 5 non-terminals'
    assert len(cfg.pos_tags) == 7, 'there are 7 POS tags'
    assert len(cfg.lhs2rhs) == 12, 'there are 12 left-hand-sides'
    for lhs in cfg.lhs2rhs.keys():
        all_rhs = cfg.lhs2rhs[lhs]
        assert np.allclose(1.0, sum([count for _, count in all_rhs])), f'probabilities of all rules with lhs = {lhs} should sum to 1'

    assert cfg.lhs2rhs['ROOT'][0][0] == 'S Period', 'the rhs of the rule with the largest probability and lhs=ROOT should be S .'
    assert np.allclose(cfg.lhs2rhs['ROOT'][0][1], 0.8333333333333334), 'the rule with the largest probability and lhs=ROOT should be 0.8333333333333334'

    assert 'Adj' in cfg.rhs2lhs['pickled'], 'pickled can be derived from Adj'
    assert 'Verb' in cfg.rhs2lhs['pickled'], 'pickled can be derived from Verb'
