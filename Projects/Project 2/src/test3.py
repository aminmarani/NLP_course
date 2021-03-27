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
    assert np.allclose(new_A[:4, 0], np.array([1.03271842e+00, 8.27926155e-05, 7.96955394e-05, 7.82777202e-05]))
    assert np.allclose(new_B[:4, 7], np.array([1.79568121e-12, 1.63529993e-12, 1.41835775e-12, 2.11401330e-13]))
    assert np.allclose(new_pi[:4], np.array([[0.00250831], [0.01328716], [0.02578417], [0.0014164 ]]))

# -------------------------------------------------------------------------
def test_maximization():
    ''' (15 points) problem3: maximization'''
    new_A = np.zeros((model.num_tags, model.num_tags))
    new_B = np.zeros((model.num_tags, model.num_words))
    new_pi = np.zeros((model.num_tags, 1))
    em_one_sentence(model, corpora.test_sentences[0], new_A, new_B, new_pi)
    maximization(model, new_A, new_B, new_pi, 0.1)
    assert np.allclose(model.A[:4, 0], np.array([0.32365755, 0.0149536, 0.01648368, 0.01856192]))
    assert np.allclose(model.B[:4, 7], np.array([5.71113895e-13, 7.66187501e-13, 1.27794044e-12, 2.33284922e-12]))
    assert np.allclose(model.pi[:4], np.array([[0.00677852], [0.02485012], [0.04444568], [0.001465]]))
