

class PrimaryWord:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def do(self, _forth):
        self.code()

    def __repr__(self):
        return f'PW: {self.name}'


class SecondaryWord:
    def __init__(self, name, word_indices):
        self.name = name
        self.word_indices = word_indices

    def do(self, forth):
        print(f'do {self.name}')
        for word_index in self.word_indices:
            forth.lexicon[word_index].do(forth)

    def __repr__(self):
        return f'SW: {self.name}'
