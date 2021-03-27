'''
    Problem 2: implement the forward, backward, and Viterbi algorithms.
    Implementation based on: http://www.cs.sjsu.edu/faculty/stamp/RUA/HMM.pdf
'''

from problem1 import *

import numpy as np

class HMM():
    """
    The HMM class that holds data structures and implementations for the forward, backward, and Viterbi algorithms.
    """

    def __init__(self, corpora):
        # self.corpora = corpora
        self.num_words = len(corpora.word_index)
        self.num_tags = len(corpora.tag_index)
        self.max_sentence_len = corpora.max_len

        # a very small positive number for Laplacian smoothing
        self.eps = 1e-8

        # for HMM parameters obtained from MLE on the POS-tagged corpus
        self.A0 = np.zeros((self.num_tags, self.num_tags)) + self.eps
        self.B0 = np.zeros((self.num_tags, self.num_words)) + self.eps
        self.pi0 = np.zeros((self.num_tags, 1)) + self.eps

        # for HMM parameters estimated iteratively during EM.
        self.A = np.zeros((self.num_tags, self.num_tags)) + self.eps
        self.B = np.zeros((self.num_tags, self.num_words)) + self.eps
        self.pi = np.zeros((self.num_tags, 1)) + self.eps

        # for forward algorithm
        self.alpha = np.zeros((self.num_tags, self.max_sentence_len))
        self.scales = np.zeros((1, self.max_sentence_len))

        # for backward algorithm
        self.beta = np.zeros((self.num_tags, self.max_sentence_len))

        # for Viterbi algorithm
        self.v = np.zeros((self.num_tags, self.max_sentence_len))
        self.back_pointer = np.zeros((self.num_tags, self.max_sentence_len))
        self.pred_seq = np.zeros((1, self.max_sentence_len))

    # -------------------------------------------------------------------------
    def mle(self, training_sentences):
        """
        Use MLE to initialize the HMM parameters A, B, and pi
        :return:
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    # -------------------------------------------------------------------------
    def forward(self, sentence):
        """
        Run the forward algorithm on a sentence and populate the alpha array.
        :param sentence: a sentence on which the forward algorithm runs. The sentence is typically from the unlabeled set. 
                        Each sentence is an array of tuples (perhaps token_key and ?)
        :return: log-likelihood, computed according to the project description using the local normalization factors.
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    # -------------------------------------------------------------------------
    def backward(self, sentence):
        """
        Run the backward algorithm on the d-th training sentence and populate the beta array
        :param sentence: a sentence on which the forward algorithm runs. The sentence is typically from the unlabeled set.
        :return:
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################

    # -------------------------------------------------------------------------
    def Viterbi(self, sentence):
        """
        Run the Viterbi algorithm on the d-th training sentence.
        Populate the v, back_point, and pred_seq arrays.
        Note that the v array stores the log of the Viterbi values to avoid underflow.

        :param sentence: a sentence on which the forward algorithm runs. The sentence is typically from the unlabeled set.
        :return: log Pr(best_Q | O)
        """
        #########################################
        ## INSERT YOUR CODE HERE
        #########################################