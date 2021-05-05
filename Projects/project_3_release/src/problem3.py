from problem1 import *
from problem2 import *
import re

class Entry():
    """
    One expansion like NP->Det Noun or Noun->president.
    Objects of this class is an element of a cell of the CYK matrix.
    """
    def __init__(self, entry_dict):
        """
        Construct a single entry, using two children entries, or a single terminal.
        :param entry_dict: a dictionary representing a derivation step.
        """
        # str representing the lhs of this derivation
        self.lhs = entry_dict['lhs']
        self.rhs_first = None
        self.rhs_second = None
        self.terminal = None

        if 'rhs_first' in entry_dict and 'rhs_second' in entry_dict:
            # extract the left and right children entries
            # pointer to the first child of type Entry
            self.rhs_first = entry_dict['rhs_first']
            # pointer to the second child of type Entry
            self.rhs_second = entry_dict['rhs_second']
        elif 'terminal' in entry_dict:
            # or just a terminal word
            self.terminal = entry_dict['terminal']


class Cell:
    """
    One cell in the CYK matrix. There can be multiple parses for the range represented by this cell.
    A cell at (i,j) of the matrix contains productions that can generate words from i to j.
    """
    def __init__(self):
        # a list of Entry objects
        self.parses = []


class CYKParser:
    """
    The CYK parser.
    Constraints:
        1) more than one productions can have the same LHS
        2) the same production can be used to construct multiple derivations in a cell.
        3) need to store back-pointers pointing to the compromising constituents of each derivation.
        4) a cell can be empty.
        5) shall facilitate CFG.rhs2lhs lookup.
    """
    def __init__(self, _cfg: CFG):
        # the grammar
        self.cfg = _cfg
        # CYK table
        self.table = {}
        # number of words in the input sentence
        self.m = 0

    def construct_larger_parses(self, left: Cell, right: Cell):
        """
        Given two cells representing adjacent ranges (e.g. [1,2] and [3,5]),
        combine them into parses covering the union of the two ranges (e.g., [1,5]).
        This is where dynamic programming happens.
        Note that there can be multiple parses that can be constructed out of the two cells.

        :param left: cell for the left range.
        :param right: cell for the right range.
        :return: a list of constructed parses, each is of Entry type. Can be an empty list.
        """
        #########################################
        #having a nested loop go over all poissible left cell and right cells and keep the matches
        res = Cell()#building an empty cell


        #if both left and right are not empty we should check all posibble matchets
        if left != [] and right != []: 
            for lc in left.parses:
                for rc in right.parses:
                    ky = ' '.join([lc.lhs,rc.lhs])
                    if ky in cfg.rhs2lhs: #find the lhs of given key (ky)
                        res.parses.append(Entry({'lhs': cfg.rhs2lhs[ky][0],
                                  'rhs_first': lc, 'rhs_second':rc}))
                        print(res.parses[0].lhs)
        # elif left != []: #only one cell and we have to check all possible "lhs => terminal" grammars

        # else:
        return res.parses
        #########################################

    def parse(self, sentence: []):
        """
        The main entry to the parsing algorithm.
        First create a dictionary table as the CYK matrix.
        A key is a tuple (i, j) and a value table[(i,j)] is a Cell, which
        represents all parses of words in the range [i, j], inclusively.
        :arg sentence: an array of terminals appear in the grammar. Can't handle unseen words!
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    def print_entry(self, entry: Entry):
        """
        Print the tree rooted at an entry to a str (not to the command line).
        Need to recursively print the child(ren) of the lhs of the entry.
        For example:
            entry = (Noun, left_entry, right_entry)
            left_entry = (Adj, 'fine')
            right_entry = (Noun, 'floor')
        Print ' (Noun (Adj fine)(Noun floor))'
        :param entry: an entry pulled from some cell of the CYK matrix.
        :return: the resulting parenthesized str.
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    def print_one_parse(self):
        """
        Output an arbitrary parsing tree re-constructed after parsing.
        :return: a parse tree if there's any.
        """
        if len(self.table[(0, self.m - 1)].parses) == 0:
            return None
        else:
            return self.print_entry(self.table[(0, self.m - 1)].parses[0])

if __name__ == '__main__':
    cfg = CFG()
    cfg.load_grammar('../data/grammar.gr')
    parser = CYKParser(cfg)

    # read in a sentence generated by the generator
    with open('../data/sentences.txt', 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            words = line.split()
            sentence = []
            for word in words:
                word = re.sub("[^a-zA-Z.!]", "", word)
                if len(word) == 0:
                    continue
                if word in cfg.terminals:
                    sentence.append(word)

            # parse the input sentence
            parser.parse(sentence)
            print(parser.print_one_parse())
