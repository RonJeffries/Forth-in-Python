

class PrimaryWord:
    def __init__(self, name, code, immediate=False):
        self.name = name
        self.code = code
        self.immediate = immediate

    def do(self, forth):
        self.code(forth)

    def __repr__(self):
        return f' {self.name}'


class SecondaryWord:
    def __init__(self, name, word_list, immediate=False):
        self.name = name
        self.words = word_list
        self.immediate = immediate
        self.pc = 0

    def do(self, forth):
        # print(self)
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

    def finish(self):
        self.pc = len(self.words)

    def __repr__(self):
        result = f'(SW: {self.name}:'
        for word in self.words:
            result += f' {word}'
        return result + ')'

