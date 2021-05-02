class CFG:
    def __init__(self):
        self.terminals = set()
        # non-terminals do not include POS tags
        self.non_terminals = set()
        self.pos_tags = set()

        # list of rules for each lhs (e.g., VP)
        # the rules for a lhs are sorted in descending order of the rule probabilities.
        self.lhs2rhs = {}

        # mapping from a word (terminal) to a set of POS tags
        self.word2tag = {}

        # mapping from a Right-Hand-Side (rhs) of a rule to a set of Left-Hand-Side (lhs).
        # the lhs (e.g., VP) for a rhs ('Verb NP') are placed in a set for quick lookup during CYK.
        self.rhs2lhs = {}

    def load_grammar(self, file_name):
        """
        Read the grammar file. Ignore the lines that contains a # or is empty.
        Each rhs is represented by a str, containing a single word, or two symbols separated by a space ' '.
        Make sure to sort the rhs's of the same lhs in descending order of the probability of the rules.
        :param file_name: path to the file containing the grammar.
        :return:
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    def symbol_type(self, symbol):
        """
        Return the type of a symbol in str type.
        if symbol is a terminal, return 0.
        if symbol is a non-termianl, return 2
        if it is a POS-tag, return 1
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################