

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
        result = f'{self.name}:'
        if self.secondary:
            for word in self.words:
                result += f' {word.name}'
        else:
            result += ' <code>'
        return result

