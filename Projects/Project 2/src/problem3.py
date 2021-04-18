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
    #initialize eta and kesi
    digamma = np.zeros((model.num_tags,model.num_tags))
    gamma = np.zeros((1,model.num_tags))
    log_p = model.forward(sentence)
    model.backward(sentence)

    for t in range(len(sentence)-1):
    	gamma = np.zeros((1,model.num_tags))
    	for i in range(model.num_tags):
    		digamma[i,:] = model.alpha[i,t] * model.A[i,:] * model.B[:,sentence[t+1][0]] * model.beta[:,t+1]
    		#gamma[0,i] += np.sum(digamma[i,:])

    	#normalize
    	digamma = digamma / np.sum(digamma)
    	gamma[0,:] = np.sum(digamma,axis=0)
    	#update new_A and new_B
    	new_A += digamma
    	new_B[:,sentence[t][0]] += gamma[0,:]
    	#update new_pi only at t=0
    	if t == 0:
    		new_pi[:,0] += np.sum(digamma,axis=1)
    		#new_pi[:,0] += gamma[0,:]


    #special case for t = T-1
    gamma[0,:] = model.alpha[:,len(sentence)-1]
    new_B[:,sentence[len(sentence)-1][0]] += gamma[0,:]



    return log_p
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
    new_A = new_A / np.sum(new_A,axis=1)
    model.A = mu * model.A + (1-mu) * new_A

    #new_B = new_B / np.sum(new_B,axis=1)
    for i in range(new_B.shape[0]):
    	new_B[i,:] = new_B[i,:] / np.sum(new_B[i,:])
    	#for o in range(new_B.shape[1]):
    	#	new_B[i,o] = new_B[i,o] / np.sum(new_B[i,:])
    model.B = mu * model.B + (1-mu) * new_B

    model.pi = mu*model.pi + (1-mu)*new_pi
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


if __name__ == 'main':
	training_path = '../data/train.txt'
	test_path = '../data/test.txt'

	corpora = Corpora()

	corpora.read_corpus(training_path, is_training=True)
	corpora.read_corpus(test_path, is_training=False)

	model = HMM(corpora)
	model.mle(corpora.training_sentences)
	em(model, corpora, 0.1, num_iters = 30)