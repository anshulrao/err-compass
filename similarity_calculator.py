import re
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec


class SentenceSimilarityCalculator:
    def __init__(self, refresh_word2vec=True):
        """
        Constructor.

        """
        self.glove_model = self._load_glove_model('glove.6B.100d.txt')  # using 10 dimension GloVe
        if refresh_word2vec: self._build_word2vec_model()
        self.word2vec_model = Word2Vec.load('word2vec.model')

    def _load_glove_model(self, glove_file):
        """
        Load GloVe pre-trained vectors.

        """
        embeddings_index = {}
        with open(glove_file, encoding="utf8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = coefs
        return embeddings_index

    def _build_word2vec_model(self):
        """
        Build intitial Word2Vec model using aved errors.

        """
        df = pd.read_csv('mappings.csv')
        sentences = df.phrase.to_list()
        base_corpus = [self._preprocess(sentence) for sentence in sentences]
        self.word2vec_model = Word2Vec(sentences=base_corpus, vector_size=100, window=5,
                                       min_count=1, workers=4)
        self.word2vec_model.save('word2vec.model')

    def _preprocess(self, sentence):
        """
        Preprocess a sentence by removing punctuation and lowercasing.
        """
        sentence = re.sub(r'[^\w\s]', '', sentence)
        return sentence.lower().split()

    def _compute_bow_similarity(self, words1, words2):
        """
        Compute similarity using Bag-of-Words model.

        """
        unique_words = set(words1 + words2)
        vector1 = [words1.count(word) for word in unique_words]
        vector2 = [words2.count(word) for word in unique_words]
        return cosine_similarity([vector1], [vector2])[0][0]

    def _compute_glove_similarity(self, words1, words2):
        """
        Computing similarity using pre-trained GloVe vectors.
        The out-of-vocabulary (OOV) words are represented with a zero vector.
        To obtain a single vector for a sentence, vectors of all words in the sentence
        are averaged.

        """
        vector1 = np.mean([self.glove_model.get(word, np.zeros(100)) for word in words1], axis=0)
        vector2 = np.mean([self.glove_model.get(word, np.zeros(100)) for word in words2], axis=0)
        return cosine_similarity([vector1], [vector2])[0][0]

    def _compute_word2vec_similarity(self, words1, words2):
        """
        Computing similarity using Word2Vec.

        """
        self.word2vec_model.build_vocab([words1], update=True)
        self.word2vec_model.train([words1],
                                  total_examples=self.word2vec_model.corpus_count,
                                  epochs=self.word2vec_model.epochs)
        vector1 = np.mean([self.word2vec_model.wv[word] for word in words1 if word in self.word2vec_model.wv],
                          axis=0)
        vector2 = np.mean([self.word2vec_model.wv[word] for word in words2 if word in self.word2vec_model.wv],
                          axis=0)
        return cosine_similarity([vector1], [vector2])[0][0]

    def compute_similarity(self, sentence1, sentence2, model=None):
        """
        Compute cosine similarity of two sentences using various methods.

        """
        words1 = self._preprocess(sentence1)
        words2 = self._preprocess(sentence2)

        if model is None:
            return {
                "BoW": self._compute_bow_similarity(words1, words2),
                "GloVe": self._compute_glove_similarity(words1, words2),
                "Word2Vec": self._compute_word2vec_similarity(words1, words2)
            }

        if model == "BoW":
            return self._compute_bow_similarity(words1, words2)
        if model == "GloVe":
            return self._compute_glove_similarity(words1, words2)
        if model == "Word2Vec":
            return self._compute_word2vec_similarity(words1, words2)
