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
                        #print(res.parses[0].lhs)
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
        #making bottom of the parsing tree (Non-Terminal -> Terminal/word)
        for i in range(len(sentence)):
            res = Cell() #make an empty cell to add details later
            for lhs in self.cfg.rhs2lhs[sentence[i]]: #read all lhs of a given term
                res.parses.append(Entry({'lhs': lhs,
                                  'terminal': sentence[i]}))
            self.table[(i,i)] = res


        #making other entries of the table
        for j in range(1,len(sentence)): #start from 1, since [(0,0)] is already filled
             #as we go from left-right using outter for, we go bottom-top using this for
            for i in reversed(range(0,j)):
                for left_ind in range(i,j): #seeking all cells on the left of (i,j)
                    for right_ind in range(i+1,j+1): #seeking all cells on the right of (i,j)
                        if i==0 and j == 4:
                            #print('0---4')
                            if left_ind == 1 and right_ind == 2:
                                # print('0---4')
                                # print((i,left_ind),(right_ind,j))
                                # print(self.table[(i,left_ind)].parses,self.table[(right_ind,j)].parses)
                                # print(self.construct_larger_parses(self.table[(i,left_ind)],self.table[(right_ind,j)]))
                            #print((i,left_ind),(right_ind,j))
                            #print('4---0')
                        #if there is possible A->BC to check
                        if (i,left_ind) in self.table.keys() and (right_ind,j) in self.table.keys():
                            #if this cell is not made before, lets create it
                            if (i,j) not in self.table.keys():
                                self.table[(i,j)] = Cell()
                            self.table[(i,j)].parses.extend( self.construct_larger_parses(self.table[(i,left_ind)],self.table[(right_ind,j)]))

                            # if self.construct_larger_parses(self.table[(i,left_ind)],self.table[(right_ind,j)]) != []:
                            #     print(i,j)
                            #     if (2,4) in self.table.keys():
                            #         print(self.table[(2,4)].parses,'2 o 4')
                            #     if i == 2 and j == 4:
                            #         print(self.table[(i,j)].parses,'@@@@')
                            #         print(self.construct_larger_parses(self.table[(i,left_ind)],self.table[(right_ind,j)])[0].lhs)
                            #         print(self.table[(i,j)].parses[0].lhs)

                        # if (i,left_ind) not in self.table.keys() or (right_ind,j) not in self.table.keys() or self.table[(i,left_ind)] == [] or self.table[(right_ind,j)] == []:
                        #     continue #there is no possible A->BC to check

                        # #print(self.table[(i,left_ind)])
                        # #go over all possible table[(i,left_ind)]
                        # for left_cell in self.table[(i,left_ind)].parses:
                        #     #go voer all possible table[(right_ind,j)]
                        #     for right_cell in self.table[(right_ind,j)].parses:
                        #         res = self.construct_larger_parses(left_cell,right_cell)
                        #         #check if previosuly we did not put the same res
                        #         if res not in self.table[(i,j)].parses:
                        #             self.table[(i,j)].parses.extend(res)
                    

                    # if (i,k) not in self.table.keys() or (k,j) not in self.table.keys() or self.table[(i,k)] == [] or self.table[(k,j)] == []:
                    #     continue #there is no possible A -> BC to check
                    # #go over all possible table[(i,k)]
                    # for left_cell in self.table[(i,k)]:
                    #     #go voer all possible table[(k,j)]
                    #     for right_cell in self.table[(k,j)]:
                    #         res = construct_larger_parses(left_cell,right_cell)
                    #         #check if previosuly we did not put the same res .............................
                    #         self.table[(i,j)].extend(res)

        #print(self.table[(0,1)].parses[0].lhs)
        print('8888888888888')
        #print(self.table[(0,0)].parses[0].lhs)
        print(self.table[(0,1)].parses[0].lhs)
        print(self.table[(2,2)].parses[0].lhs)
        print(self.table[(3,4)].parses[0].lhs)
        print(self.table[(2,4)].parses[0].lhs)
        print(self.table[(0,4)].parses[0].lhs)
        print(self.table[(5,5)].parses[0].lhs)
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
        return ' '+self.print_rec(entry)
        #########################################

    def print_rec(self, entry: Entry):
        if entry.rhs_first != None and entry.rhs_second != None:
            s = '(' + entry.lhs
        #print(node.symbol)
        #if node.leftChild != None:
            s+= ' '+ self.print_rec(entry.rhs_first)
        #if node.rightChild != None:
            s+= ' ' + self.print_rec(entry.rhs_second)

            s += ')'

            return s
        else:
            return '(' + entry.lhs + ' ' + entry.terminal + ')'

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

            parser.m = len(sentence)
            print(sentence,'-----sentence')
            # parse the input sentence
            parser.parse(sentence)
            print(parser.table[(0,5)].parses,'  ----parses')
            print(parser.print_one_parse())
