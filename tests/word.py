

class PrimaryWord:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def do(self, forth):
        self.code(forth)

    def __repr__(self):
        return f'PW: {self.name}'


class SecondaryWord:
    def __init__(self, name, word_list):
        self.name = name
        self.words = word_list
        self.pc = 0

    def do(self, forth):
        forth.begin(self)
        self.pc = 0
        while self.pc < len(self.words):
            w =  self.next_word()
            w.do(forth)
        forth.end()

    def next_word(self):
        word =  self.words[self.pc]
        self.pc += 1
        return word

    def skip(self, n):
        self.pc += n

    def __repr__(self):
        return f'SW: {self.name}'
