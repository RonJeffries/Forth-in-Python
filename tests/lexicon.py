
class Lexicon:
    def __init__(self):
        self.lexicon = []

    def append(self, word):
        self.lexicon.append(word)

    def find_word(self, word):
        return next(filter(lambda d: d.name == word, reversed(self.lexicon)), None)

