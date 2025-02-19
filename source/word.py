

class Word:
    def __init__(self, name, word_list, immediate=False, secondary=True):
        self.name = name
        self.words = word_list
        self.immediate = immediate
        self.secondary = secondary
        self.pc = 0

    def append(self, word):
        self.words.append(word)

    def __call__(self, forth):
        if self.secondary:
            forth.begin(self)
        self.pc = 0
        while self.pc < len(self.words):
            w =  self.next_word()
            w(forth)
        if self.secondary:
            forth.end()

    def index(self, word_name, start=0):
        for i, word in enumerate(self.words[start:]):
            if type(word) == Word and word.name == word_name or word == word_name:
                return i + start
        return None

    def branch(self, word_address):
        self.pc = word_address

    def next_word(self):
        word =  self.words[self.pc]
        self.pc += 1
        return word

    def skip(self, n):
        self.pc += n

    def copy_to_latest(self, lexicon):
        latest = lexicon.latest_word()
        while self.pc < len(self.words):
            w = self.next_word()
            latest.append(w)

    def __repr__(self):
        if self.secondary:
            result = f': {self.name}'
            for word in self.words:
                if type(word) is Word:
                    result += f' {word.name}'
                else:
                    result += f' {word}'
            result += ' ;'
        else:
            result = self.name # + ': <code>'
        return result

