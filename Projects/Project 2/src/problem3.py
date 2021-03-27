'''
    Problem 3: EM for HMM training
        Use functions in problem1.py and problem2.py to run EM algorithm and train/evaluate HMM.
'''

from problem2 import *

import numpy as np

# -------------------------------------------------------------------------
def em(model, corpora, mu, num_iters = 30):
    """
    The EM algorithm for training HMM.
    :param model: the HMM model to be trained
    :param corpora: training and test corpora
    :param mu: relative importance of MLE
    :param num_iters: number of total EM iterations
    :return:
    """

    # initialize model parameters using the POS-tagged sentences
    model.mle(corpora.training_sentences)

    for it in range(num_iters):
        # reset the ksi and gamma matrices and get ready for accumulation of the soft frequencies

        # new_= np.zeros((model.num_tags, 1))
        new_A = np.zeros((model.num_tags, model.num_tags))
        new_B = np.zeros((model.num_tags, model.num_words))
        new_pi = np.zeros((model.num_tags, 1))

        # the E-step: go through the unlabeled corpus and update the ksi & gamma matrices
        log_likelihood = 0
        for i, sentence in enumerate(corpora.test_sentences):
            log_likelihood += em_one_sentence(model, sentence, new_A, new_B, new_pi)
        print(log_likelihood)
        # normalize new_A, new_B, and new_pi
        # update HMM parameters A, B, and pi using the new_A, new_B, and new_pi
        maximization(model, new_A, new_B, new_pi, mu)

        accuracy, log_p = evaluate(model, corpora.test_sentences)
        print(accuracy, log_p)

# -------------------------------------------------------------------------
def em_one_sentence(model, sentence, new_A, new_B, new_pi):
    """
    Run the expectation step using the fixed HMM model on a single sentence.
    The soft fraquencies are accumulated into the last four matrices.
    :param model: the current fixed HMM
    :param sentence: a sentence from test set, presumably unlabeled.
    :param new_A: sum of transition soft frequencies (tag_i -> tag_j)
    :param new_B: sum of emission soft frequencies (tag_i -> word_o)
    :param new_pi: sum of starting soft frequencies (tag_i)
    :return: log likelihood obtained from the forward algorithm
    """
    #########################################
    ## INSERT YOUR CODE HERE
    #########################################


# -------------------------------------------------------------------------
def maximization(model, new_A, new_B, new_pi, mu):
    """
    Update HMM parameters A, B, and pi
    :param model:
    :param new_A:
    :param new_B:
    :param new_pi:
    :param mu: a real number between [0, 1]. Relative importance of the MLE
    :return:
    """
    #########################################
    ## INSERT YOUR CODE HERE
    #########################################


# -------------------------------------------------------------------------
def evaluate(model, test_corpus):
    """
    Use Viterbi algorithm to predict POS tags for the sentences in the test_corpus.
    :param model: an HMM
    :param test_corpus: list of POS-tagged sentences
    :return: accuracy of the prediction, defined as the percentage of tags that are predicted correctly.
    """
    correct = 0.0
    total = 0.0
    total_log_p = 0
    for sentence in test_corpus:
        max_log_p = model.Viterbi(sentence)
        total_log_p += max_log_p
        for t, (o, q) in enumerate(sentence):
            if model.pred_seq[0, t] == q:
                correct += 1.0
        total += len(sentence)
    return correct / total, total_log_p