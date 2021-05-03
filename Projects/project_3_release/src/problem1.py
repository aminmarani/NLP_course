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
        ########################################
        with open(file_name,'r') as f:
            for line in f:
                if (line[0] != '#' and len(line)>3): #if this line starts with '#' or is shorter than length of 3 skip it
                    line = line[0:-1] #removing \n
                    arr = line.split('\t')
                    #there is a bug in grammar and two last rules are separated using two spaces not tabs
                    if len(arr) == 1:
                        arr = line.split('   ')
                    #if len(arr[2].split(' ')) > 1: #the rhs consists of 2 non-terminals
                    #adding lhs2rhs
                    if arr[1] in self.lhs2rhs.keys(): #an exisiting key
                        t = self.lhs2rhs[arr[1]]
                        t.append([' '.join(arr[2:3]),float(arr[0])])
                        self.lhs2rhs[arr[1]] = t
                    else: #a new key
                        self.lhs2rhs[arr[1]] = [[' '.join(arr[2:3]),float(arr[0])]]
                        #adding non-terminal
                        if arr[1].isupper(): #a Non-terminal has all upper-case letters
                            self.non_terminals.add(arr[1])

                    if len(arr[2].split(' ')) == 1:#len(arr) == 3: #terminal grammar --> add word2tag
                        if arr[2] in self.word2tag.keys() and arr[1] not in self.word2tag[arr[2]]:
                            t = self.word2tag[arr[2]]
                            t.append(arr[1])
                            self.word2tag[arr[2]] = t
                        elif arr[2] not in self.word2tag.keys():
                            self.word2tag[arr[2]] = [[arr[1]]]
                            #time to add a terminal
                            self.terminals.add(arr[2])
                        #add postags
                        self.pos_tags.add(arr[1])

                    #adding rhs2lhs
                    rhs_key = ' '.join(arr[2:3])
                    if  rhs_key in self.rhs2lhs.keys():
                        t = self.rhs2lhs[rhs_key]
                        t.append(arr[1])
                        self.rhs2lhs[rhs_key] = t
                    else:
                        self.rhs2lhs[rhs_key] = [arr[1]]


        #go over self.lhs2rhs and recompute all probabilities
        for ky in self.lhs2rhs.keys():
            s = 0
            for i in range(len(self.lhs2rhs[ky])):
                s += self.lhs2rhs[ky][i][1]
            for i in range(len(self.lhs2rhs[ky])):
                self.lhs2rhs[ky][i][1] = self.lhs2rhs[ky][i][1] / s
            #time to sort every single item of this key
            self.lhs2rhs[ky] = sorted(self.lhs2rhs[ky],key= lambda x: x[1] ,reverse=True)


        #########################################

    def symbol_type(self, symbol):
        """
        Return the type of a symbol in str type.
        if symbol is a terminal, return 0.
        if symbol is a non-termianl, return 2
        if it is a POS-tag, return 1
        """
        #########################################
        if symbol in self.terminals:
            return 0
        if symbol in self.non_terminals:
            return 2
        if symbol in self.pos_tags:
            return 1
        return -1
        #########################################



grammar_path = '../data/grammar.gr'
cfg = CFG()
cfg.load_grammar(grammar_path)