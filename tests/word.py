

class PrimaryWord:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def do(self, forth):
        self.code(forth)

    def __repr__(self):
        return f'PW: {self.name}'


class SecondaryWord:
    # why don't we just store the word in the lexicon? it's no larger than the index.
    def __init__(self, name, word_indices):
        self.name = name
        self.word_indices = word_indices
        self.ix = 0

    def do(self, forth):
        forth.begin(self)
        lexicon = forth.lexicon
        self.ix = 0
        while self.ix < len(self.word_indices):
            word_index = self.word_indices[self.ix]
            lexicon[word_index].do(forth)
            self.ix += 1
        forth.end()

    def skip(self, n):
        self.ix += n

    def __repr__(self):
        return f'SW: {self.name}'
