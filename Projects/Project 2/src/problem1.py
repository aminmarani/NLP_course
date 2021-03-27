'''
    Problem 1: data pre-processing.
        Define the basic data structures to hold training and test corpora.
        Read in training corpus and build word-index and pos_tag-index mappings
'''

class Corpora():
    """
    The class holding training and test corpora.
    """

    def __init__(self):
        """
        Constructor
        """
        # word to index (0-based integers) mapping
        self.word_index = {}
        # POS-tag to index (0-based integers) mapping
        self.tag_index = {}
        # index to POS-tag mapping: the reverse mapping of the above
        self.index_tag = {}
        # list of sentences, each of which is a list of pairs of integer indices (word_index[w_t], tag_index[tag_t]),
        # where w_t and tag_t are the word and POS tag at the location t of a sentence, respectively.
        self.training_sentences = []
        # list of sentences, each of which is a list of integer indices (word_index[w_t])
        self.test_sentences = []

        self.max_len = 0

    # -------------------------------------------------------------------------
    def read_corpus(self, corpus_path, is_training):
        """
        Read a corpus
        :param corpus_path: path to a file with POS-tagged sentences.
        :param is_training: if true, the file is for the training corpus, otherwise the test corpus
        :return:
        """
        with open(corpus_path, 'r') as f:
            # holding the current sentence
            cur_sentence = []
            self.max_len = 0
            while True:
                # each line is a (word, POS_tag, other_label) tuple.
                line = f.readline()
                if not line:
                    break
                # sentences are delimited by an empty line.
                if len(line) == 1:
                    if is_training:
                        self.training_sentences.append(cur_sentence)
                    else:
                        self.test_sentences.append(cur_sentence)
                    if len(cur_sentence) > self.max_len:
                        self.max_len = len(cur_sentence)
                    cur_sentence = []
                    continue
                w, t, _ = line.strip().split()
                if w not in self.word_index:
                    self.word_index[w] = len(self.word_index)
                if t not in self.tag_index:
                    self.tag_index[t] = len(self.tag_index)
                    self.index_tag[len(self.tag_index) - 1] = t
                cur_sentence.append((self.word_index[w], self.tag_index[t]))