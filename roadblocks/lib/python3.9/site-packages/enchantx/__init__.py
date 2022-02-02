import numpy as np

from enchant import Dict
from enchantx.vectorizer import WORD2VEC


class XDict:

    def __init__(self, model_path=None, tag=None, broker=None):
        self.enchant_obj = Dict(tag=tag, broker=broker)
        self.enchantX = WORD2VEC(model_path)

    def check(self, word) -> bool:
        return self.enchant_obj.check(word)

    def suggest(self, word) -> list:
        return self.enchant_obj.suggest(word)

    def smart_suggest(self, word: str, next_word: str) -> list:
        if self.check(word):
            return []
        if not next_word:
            return []
        suggested_words = self.suggest(word)
        if len(suggested_words) > 0:
            distances = self.enchantX.calculate_distances(next_word, suggested_words)

            if distances.size == 0:
                return suggested_words
            else:
                words_with_score = dict()
                for word, dist in zip(suggested_words, list(distances)):
                    words_with_score[word] = dist
                return sorted(words_with_score, key=words_with_score.get)

        else:
            return []

    def smart_suggest_with_scores(self, word: str, next_word: str) -> dict:
        if self.check(word):
            return {}

        suggested_words = self.suggest(word)
        if len(suggested_words) > 0:
            distances = self.enchantX.calculate_distances(next_word, suggested_words)

            if distances.size == 0:
                return {}
            else:
                words_with_score = dict()
                for word, dist in zip(suggested_words, list(distances)):
                    if not np.isnan(dist):
                        words_with_score[word] = dist

                suggestions = dict()
                for word, dist in sorted(words_with_score.items(), key=lambda tup: tup[1]):
                    suggestions[word] = int(round(1 - dist, 2)*100)
                return suggestions

        else:
            return {}