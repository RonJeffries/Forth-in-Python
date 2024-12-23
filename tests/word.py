

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
        self.pc = 0

    def do(self, forth):
        forth.begin(self)
        lexicon = forth.lexicon
        self.pc = 0
        while self.pc < len(self.word_indices):
            self.next_word().do(forth)
        forth.end()

    def next_word(self):
        word =  self.word_indices[self.pc]
        self.pc += 1
        return word

    def skip(self, n):
        self.pc += n

    def __repr__(self):
        return f'SW: {self.name}'
