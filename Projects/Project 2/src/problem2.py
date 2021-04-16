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
        Use MLE to initialize the HMM parameters A, B, and pi and A0, B0, and pi0
        :return:
        """
        #########################################
        ## INSERT YOUR CODE HERE
        import copy #using deepcopy (we can also use A = A0[:,:])
        #each training_sentences entry is (word index,tag index)

        #A dictionary to keep #(qt=i) for qt=i and qt+1=j
        occurences = {}
        #A dictionary to keep #(qt=i) for qt=i and Ot=o
        occurences_O = {}

        for sentence in training_sentences:
            for i in range(len(sentence)):
                o = sentence[i][0] #O_i
                qt = sentence[i][1] #q_i
                if i < len(sentence) -1: #we don't update qt+1 and A0 for t+1 at last i
                    qt1 = sentence[i+1][1] #q_j
                    #updating the parameters
                    self.A0[qt,qt1] += 1 #add one to A_ij
                    #keeping the number of occurences for (qt=i)
                    if qt in occurences.keys():
                        occurences[qt] += 1
                    else:
                        occurences[qt] = 1

                #updating the parameters
                self.B0[qt,o] += 1 #add one to B_ij
                #keeping the number of occurences for (qt=i)
                if qt in occurences_O.keys():
                    occurences_O[qt] += 1
                else:
                    occurences_O[qt] = 1

                
            #updating pi_i
            self.pi0[sentence[0][1],0] += 1

        #updating A0 and B0 using the occurences for each q_t=i
        for k in occurences.keys():
            self.A0[k,:] = self.A0[k,:] / occurences[k]
            self.B0[k,:] = self.B0[k,:] / (occurences_O[k]+self.eps*self.B0.shape[1])

        #updating PI
        self.pi0 = self.pi0 / len(training_sentences)

        self.A = self.A0[:,:]
        self.pi = self.pi0[:,:]
        self.B = self.B0[:,:]
        #########################################

    # -------------------------------------------------------------------------
    def forward(self, sentence):
        """
        Run the forward algorithm on a sentence and populate the alpha array.
        :param sentence: a sentence on which the forward algorithm runs. The sentence is typically from the unlabeled set.
        :return: log-likelihood, computed according to the project description using the local normalization factors.
        """
        #########################################
        ## INSERT YOUR CODE HERE
        res = 0
        c0 = 0
        T = len(sentence)
        N = self.num_tags
        #initializing alpha
        alpha = np.zeros((N,self.max_sentence_len)) #T*N (T observation and N hidden states)
        #computing alpha[0,:]
        # for i in range(N):
        #     #o,t = sentence[i]
        #     alpha[0,i] = self.pi[i] * self.B[i,0]
        #     c0 += alpha[0,i]
        alpha[:,0] = self.pi[:].T * self.B[:,sentence[0][0]]
        c0 = np.sum(alpha[:,0])
        res = -1 * np.log(c0)

        #scale the alpha[0,:]
        c0 = 1/c0
        self.scales[0,0] = c0
        alpha[:,0] = c0 * alpha[:,0]

        #compute alpha[t,i]
        for t in range(1,T):
            ct = 0
            for i in range(N):
                #alpha[t,i] = 0
                # for j in range(N):
                #     alpha[t,i] += alpha[t-1,j] * self.A[j,i]
                alpha[i,t] = np.sum(alpha[:,t-1]*self.A[:,i])
                alpha[i,t] = alpha[i,t]*self.B[i,sentence[t][0]]
                ct += alpha[i,t]
            res += -1 * np.log(ct)
            #scale alpha
            ct = 1/ct
            self.scales[0,t] = ct
            alpha[:,t] = ct * alpha[:,t]


        self.alpha = alpha[:,:]

        return -1*res
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