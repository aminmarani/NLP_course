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
                    if self.A0[qt,qt1]>=1.0: #that means it is already initialized by the first occurence
                        self.A0[qt,qt1] += 1 #add one to A_ij
                    else: #otherwise we have to initiate it with 1 to get rid of eps
                        self.A0[qt,qt1] = 1
                    #keeping the number of occurences for (qt=i)
                    if qt in occurences.keys():
                        occurences[qt] += 1
                    else:
                        occurences[qt] = 1

                

                #updating the parameters
                if self.B0[qt,o]>=1.0: #that means it is already initialized by the first occurence
                    self.B0[qt,o] += 1 #add one to B_ij
                else: #otherwise we have to initiate it with 1 to get rid of eps
                    self.B0[qt,o] = 1 
                #keeping the number of occurences for (qt=i)
                if qt in occurences_O.keys():
                    occurences_O[qt] += 1
                else:
                    occurences_O[qt] = 1

                
            #updating pi_i
            if self.pi0[sentence[0][1],0] < 1.0:
                self.pi0[sentence[0][1],0] = 1
            else:
                self.pi0[sentence[0][1],0] += 1

            # print(sentence)
            # print(occurences)
            # print(occurences_O)
            # return 0

        #updating A0 and B0 using the occurences for each q_t=i
        for k in occurences.keys():
            for j in range(self.num_tags):
                self.A0[k,j] = self.A0[k,j] / occurences[k]
            for j in range(self.num_words):
                self.B0[k,j] = self.B0[k,j] / (occurences_O[k]+self.eps*self.B0.shape[1])

        #updating PI
        self.pi0 = self.pi0 / len(training_sentences)

        self.A = self.A0[:,:]
        self.pi = self.pi0[:,:]
        self.B = self.B0[:,:]

        ###print(self.A[0, 0:2])
        ###print(np.sum(self.B, axis=1))

        # #Dictionaries to keep track of co-occurences and frequencies
        # qq_occ = {} 
        # qo_occ = {}
        # qq_term = {}
        # qo_term = {}
        # q1_occ = {}

        # for sentence in training_sentences:
        #     for t in range(len(sentence)-1): #we don't consider last one for A_ij
        #         qt = sentence[t][1]
        #         ot = sentence[t][0]
        #         qt1 = sentence[t+1][1]

        #         #adding to dictionaries
        #         if (qt,qt1) in qq_occ.keys():
        #             qq_occ[qt,qt1] +=1 
        #         else:
        #             qq_occ[qt,qt1] =1 

        #         if (qt,ot) in qo_occ.keys():
        #             qo_occ[qt,ot] += 1
        #         else:
        #             qo_occ[qt,ot] = 1

        #         if qt in qq_term.keys():
        #             qq_term[qt] += 1
        #         else:
        #             qq_term[qt] = 1

        #         if qt in qo_term.keys():
        #             qo_term[qt] += 1
        #         else:
        #             qo_term[qt] = 1

            
        #     #adding last T in qo_occ and qo_term
        #     qt = sentence[-1][1]
        #     ot = sentence[-1][0]
        #     if (qt,ot) in qo_occ.keys():
        #         qo_occ[qt,ot] += 1
        #     else:
        #         qo_occ[qt,ot] = 1

        #     if qt in qo_term.keys():
        #         qo_term[qt] += 1
        #     else:
        #         qo_term[qt] = 1

        #     #counting q1=i
        #     if sentence[0][1] in q1_occ.keys():
        #         q1_occ[sentence[0][1]] += 1
        #     else:
        #         q1_occ[sentence[0][1]] = 1

        # for k,v in qq_occ.items():
        #     self.A[k[0],k[1]] = v/qq_term[k[0]]

        # for k,v in qo_occ.items():
        #     self.B[k[0],:] = self.B[k[0],:]/qo_term[k[0]]
        # for k,v in qo_occ.items():
        #     self.B[k[0],k[1]] = v/qo_term[k[0]]
        

        # for k,v in q1_occ.items():
        #     self.pi[k] = v/len(training_sentences)


        # # for i in range(self.B.shape[0]):
        # #     self.B[i,:] = self.B[i,:] / np.sum(self.B[i,:])


        # self.A0[:,:] = self.A[:,:]
        # self.B0[:,:] = self.B[:,:]
        # self.pi0[:,:] = self.pi



        # print(self.B[0,0:10])
        # print(np.sum(self.B, axis=1))


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
        #let beta_T-1(i) = 1, scaled by C_T-1
        T = len(sentence)
        N = self.num_tags
        #initializing alpha
        beta = np.zeros((N,self.max_sentence_len))
        beta[:,T-1] = self.scales[0,T-1]

        #beta-pass
        for t in reversed(range(0,T-1)):
            for i in range(N):
                beta[i,t] = np.sum(self.A[i,:]*self.B[:,sentence[t+1][0]]*beta[:,t+1])
                beta[i,t] = beta[i,t] * self.scales[0,t]
                # for j in range(N):
                #     beta[]

        self.beta = beta[:,:]

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
        T = len(sentence)
        N = self.num_tags
        #initializing viterbi and backpointers
        viterbi = np.zeros((N,self.max_sentence_len))
        viterbi2 = np.zeros((N,self.max_sentence_len))
        backpointers = np.zeros((N,self.max_sentence_len))

        viterbi[:,0] = self.pi[0,:] * self.B[:,sentence[0][0]]
        viterbi[:,0] = np.log(self.pi[0,:]) + np.log(self.B[:,sentence[0][0]])

        #recursion step
        for t in range(1,T):
            for s in range(N):
                #viterbi[s,t] = np.max(viterbi[:,t-1] * self.A[:,s] * self.B[s,sentence[t][0]])
                viterbi[s,t] = np.max( (viterbi[:,t-1]) + np.log(self.A[:,s]) + np.log(self.B[s,sentence[t][0]]))
                backpointers[s,t] = np.argmax( (viterbi[:,t-1]) + np.log(self.A[:,s]) + np.log(self.B[s,sentence[t][0]]))
                #backpointers[s,t] = np.argmax(viterbi[:,t-1] * self.A[:,s] * self.B[s,sentence[t][0]])

        # for t in range(4):
        #     #print(backpointers[:,t])
        #     print((viterbi[:,t]))


        bestpathprob = np.max(viterbi[:,T-1]) #T-1 = the last item in the Viterbi
        bestpathpointer = np.argmax(viterbi[:,T-1]) 

        #print(bestpathpointer)
        #finding best path
        bestpath = np.zeros((1,self.max_sentence_len)) #initilize with zeros
        #set last step t=T (or T-1 actually) to bestpathpointer
        bestpath[0,T-1] = bestpathpointer

        for t in reversed(range(1,T)): #getting back from last observation (T) to first (O0)
            bestpath[0,t-1] = backpointers[int(bestpath[0,t]),t]

        self.pred_seq[0,:] = bestpath[:,:]
        self.v = viterbi[:,:]
        self.backpointers = backpointers[:,:]

        #print(bestpath)
        return bestpathprob
        #########################################