from problem1 import *
from problem2 import *
from problem3 import *

'''
    Unit test 3:
    This file includes unit tests for problem3.py.
    You could test the correctness of your code by typing `nosetests -v test3.py` in the terminal.
'''
grammar_path = '../data/grammar.gr'
cfg = CFG()
cfg.load_grammar(grammar_path)
parser = CYKParser(cfg)

def test_construct_larger_parses():
    """ (15 points) problem3: selectRule """
    left = Cell()
    left.parses.append(Entry({'lhs': 'Verb',
                              'terminal': 'pickled'}))
    left.parses.append(Entry({'lhs': 'Adj',
                              'terminal': 'pickled'}))
    right = Cell()
    right.parses.append(Entry({'lhs': 'Noun',
                              'terminal': 'president'}))

    for e in parser.construct_larger_parses(left, right):
        assert e.lhs == 'Noun'
        assert e.rhs_first.lhs == 'Adj'
        assert e.rhs_second.lhs == 'Noun'
        assert e.terminal is None

def test_parse():
    """ (15 points) problem3: selectRule """
    sentence = ['perplexed', 'president']
    parser.parse(sentence)

    assert parser.table[(0,1)].parses[0].lhs == 'Noun'
    assert parser.table[(0,1)].parses[0].rhs_first.lhs == 'Adj'
    assert parser.table[(0,1)].parses[0].rhs_second.lhs == 'Noun'

def test_print_entry():
    """ (15 points) problem3: selectRule """
    e1 = Entry({'lhs': 'Adj',
            'terminal': 'pickled'})
    assert e1.lhs == 'Adj'
    assert e1.terminal == 'pickled'
    assert parser.print_entry(e1) == ' (Adj pickled)'

    e2 = Entry({'lhs': 'Noun',
                'terminal': 'president'})
    assert e2.lhs == 'Noun'
    assert e2.terminal == 'president'
    assert parser.print_entry(e2) == ' (Noun president)'

    e3 = Entry({'lhs': 'Noun',
               'rhs_first': e1,
               'rhs_second': e2})
    assert parser.print_entry(e3) == ' (Noun (Adj pickled) (Noun president))'