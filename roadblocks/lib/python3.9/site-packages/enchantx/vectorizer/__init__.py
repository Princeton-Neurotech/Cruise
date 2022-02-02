import logging
import os

import numpy as np

from gensim.models import KeyedVectors
from six import string_types


logging.basicConfig(filename="vectorizer.log")
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.WARNING)


class WORD2VEC:
    _default_path_to_model = "GoogleNews-vectors-negative300.bin"

    def __init__(self, path_to_model=None):
        if path_to_model:
            self.word2vec = _WORD2VEC(path_to_model)
        elif WORD2VEC._default_path_to_model in os.listdir(os.getcwd()):
            self.word2vec = _WORD2VEC(os.path.join(os.getcwd(), WORD2VEC._default_path_to_model))
        elif WORD2VEC._default_path_to_model in os.listdir(os.path.expanduser("~/.enchantx")):
            self.word2vec = _WORD2VEC(os.path.join(os.path.expanduser("~/.enchantx"), WORD2VEC._default_path_to_model))
        else:
            raise FileNotFoundError("Couldn't find the file - GoogleNews-vectors-negative300.bin. Plese provide the valid path.")

    def calculate_distances(self, word_or_vector, other_words) -> np.array:
        if isinstance(word_or_vector, string_types):
            try:
                input_vector = self.word2vec[word_or_vector]
            except KeyError as exp:
                logger.warning(exp)
                return np.asarray([])
        else:
            input_vector = word_or_vector
        if not other_words:
            return np.asarray([])
        else:
            other_vectors = []
            for word in other_words:
                try:
                    other_vectors += [self.word2vec[word]]
                except KeyError as exp:
                    logger.warning(exp)
                    other_vectors += [np.zeros((300,))]

            other_vectors = np.asarray(other_vectors)
            return 1 - self.word2vec.cosine_similarities(input_vector, other_vectors)


class _WORD2VEC:

    class __OnlyOne:
        def __init__(self, path_to_bin: str):
            self.path_to_binary_model = path_to_bin
            try:
                self.word2vec = KeyedVectors.load_word2vec_format(self.path_to_binary_model, binary=True)
            except Exception as exp:
                raise ImportError(exp)

        def __str__(self):
            return "Loaded word2vec: {}".format(self.path_to_binary_model)

    instance = None

    def __new__(cls, *args, **kwargs):
        if not _WORD2VEC.instance:
            if len(args) != 0:
                _WORD2VEC.instance = _WORD2VEC.__OnlyOne(path_to_bin=args[0])
            else:
                raise FileNotFoundError("Please provide valid path for the pretrained model")
        return _WORD2VEC.instance
