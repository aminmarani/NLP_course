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
    assert np.allclose(new_A[:4, 0], np.array([4.72981557e-04, 1.59845908e-09, 6.32529586e-09, 1.12443252e-09]), atol=1e-9)
    assert np.allclose(new_B[:4, 7], np.array([3.38837699e-11, 2.23475084e-12, 1.39241478e-14, 1.31380688e-10]), atol=1e-9)
    assert np.allclose(new_pi[:4], np.array([[0.00034521], [0.01833199], [0.03044146], [0.00059843]]), atol=1e-9)

# -------------------------------------------------------------------------
def test_maximization():
    ''' (15 points) problem3: maximization'''
    new_A = np.zeros((model.num_tags, model.num_tags))
    new_B = np.zeros((model.num_tags, model.num_words))
    new_pi = np.zeros((model.num_tags, 1))
    em_one_sentence(model, corpora.test_sentences[0], new_A, new_B, new_pi)
    maximization(model, new_A, new_B, new_pi, 0.1)
    assert np.allclose(model.A[:4, 0], np.array([0.0119059, 0.01115603, 0.04845907, 0.00395955]), atol=1e-9)
    assert np.allclose(model.B[:4, 7], np.array([9.92441232e-12, 9.14512240e-13, 6.66963758e-14, 1.00123541e-09]), atol=1e-9)
    assert np.allclose(model.pi[:4], np.array([[0.00483173], [0.02939046], [0.04863724], [0.00072883]]), atol=1e-9)
