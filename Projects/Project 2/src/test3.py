from problem3 import *

'''
    Unit test 3:
    This file includes unit tests for problem3.py.
    You could test the correctness of your code by typing `nosetests -v test3.py` in the terminal.
'''
training_path = '../data/train.txt'
test_path = '../data/test.txt'

corpora = Corpora()

corpora.read_corpus(training_path, is_training=True)
corpora.read_corpus(test_path, is_training=False)

model = HMM(corpora)
model.mle(corpora.training_sentences)
log_p = model.forward(corpora.test_sentences[0])
model.backward(corpora.test_sentences[0])
model.Viterbi(corpora.test_sentences[0])
new_A = np.zeros((model.num_tags, model.num_tags))
new_B = np.zeros((model.num_tags, model.num_words))
new_pi = np.zeros((model.num_tags, 1))

# em_one_sentence(model, corpora.test_sentences[0], new_A, new_B, new_pi)
# print(new_A[:4, 0])
# print(new_B[:4, 7])
# print(new_pi[:4])
#
# maximization(model, new_A, new_B, new_pi, 0.1)
# print(model.A[:4, 0])
# print(np.nonzero(np.sum(model.B, axis = 0)))
# print(model.B[:4, 7])
# print(model.pi[:4])

# -------------------------------------------------------------------------
def test_em_one_sentence():
    ''' (20 points) problem3: em_one_sentence'''
    new_A = np.zeros((model.num_tags, model.num_tags))
    new_B = np.zeros((model.num_tags, model.num_words))
    new_pi = np.zeros((model.num_tags, 1))
    em_one_sentence(model, corpora.test_sentences[0], new_A, new_B, new_pi)
    assert np.allclose(new_A[:4, 0], np.array([1.00305608e+00, 4.12195636e-04, 8.09206178e-04, 5.09656527e-05]))
    assert np.allclose(new_B[:4, 7], np.array([2.12883778e-11,1.40554975e-12, 9.29618949e-15, 8.25087270e-11]))
    assert np.allclose(new_pi[:4], np.array([[0.0003452 ], [0.01833159], [0.03044079], [0.00059841]]))

# -------------------------------------------------------------------------
def test_maximization():
    ''' (15 points) problem3: maximization'''
    new_A = np.zeros((model.num_tags, model.num_tags))
    new_B = np.zeros((model.num_tags, model.num_words))
    new_pi = np.zeros((model.num_tags, 1))
    em_one_sentence(model, corpora.test_sentences[0], new_A, new_B, new_pi)
    maximization(model, new_A, new_B, new_pi, 0.1)
    assert np.allclose(model.A[:4, 0], np.array([0.30876305, 0.0113152, 0.04916039, 0.00439564]))
    assert np.allclose(model.B[:4, 7], np.array([6.33645381e-12, 5.86694412e-13, 6.25974007e-14, 7.06212818e-10]))
    assert np.allclose(model.pi[:4], np.array([[0.00483172], [0.0293901], [0.04863664], [0.00072881]]))
