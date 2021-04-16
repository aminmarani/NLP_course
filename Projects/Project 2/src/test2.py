from problem2 import *

'''
    Unit test 1:
    This file includes unit tests for problem2.py.
    You could test the correctness of your code by typing `nosetests -v test2.py` in the terminal.
'''
training_path = '../data/train.txt'
test_path = '../data/test.txt'

corpora = Corpora()

corpora.read_corpus(training_path, is_training=True)
corpora.read_corpus(test_path, is_training=False)

# a = corpora.training_sentences[0]
# print(a)
# print(corpora.training_sentences[0])
# print(corpora.test_sentences[0])
# exit()

model = HMM(corpora)
model.mle(corpora.training_sentences)
log_p = model.forward(corpora.test_sentences[0])
model.backward(corpora.test_sentences[0])
max_log_p = model.Viterbi(corpora.test_sentences[0])
# print(model.pred_seq)
# print(max_log_p)
# -------------------------------------------------------------------------
def test_mle():
    ''' (15 points) problem2: mle'''
    assert np.allclose(np.nonzero(np.sum(model.B, axis = 0))[0][:10], np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    assert np.allclose(model.A[0, 0:2], np.array([0.11767829, 0.2478346]))
    assert np.allclose(model.pi[0:2, 0], np.array([0.04521038, 0.12891674]))
    assert np.allclose(np.sum(model.A, axis=1), np.ones((model.num_tags, 1)))
    assert np.allclose(np.sum(model.B, axis=1), np.ones((model.num_tags, 1)))
    assert np.allclose(np.sum(model.pi), 1)
    assert np.allclose(model.A, model.A0)
    assert np.allclose(model.B, model.B0)
    assert np.allclose(model.pi, model.pi0)

# -------------------------------------------------------------------------
def test_forward():
    ''' (15 points) problem2: forward'''
    assert np.allclose(model.alpha[:5, 0], np.array([0.00455201, 0.01718975, 0.03516259, 0.00124236, 0.02771086]))
    assert np.allclose(np.sum(model.alpha[:, :len(corpora.test_sentences[0])], axis = 0), np.ones((1, len(corpora.test_sentences[0]))))
    assert np.allclose(log_p, -248.70719542854852)
    assert np.allclose(model.scales[0, :5], np.array([3.03534949e+11, 2.06774131e+03, 1.91007373e+02, 2.17765633e+01, 1.63654423e+05]))

# -------------------------------------------------------------------------
def test_backward():
    ''' (15 points) problem2: backward'''
    assert np.allclose(model.beta[:5, 0], np.array([0.12389497, 2.30733333, 2.32553277, 5.10405791, 0.39604281]))

# -------------------------------------------------------------------------
def test_Viterbi():
    ''' (20 points) problem2: Viterbi'''
    max_log_p = model.Viterbi(corpora.test_sentences[0])
    assert np.allclose(model.pred_seq[0, :4], np.array([42, 10, 10, 13]))
    assert max_log_p == -251.33681313848558
