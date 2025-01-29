

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

    def append(self, word):
        self.words.append(word)

    def do(self, forth):
        forth.begin(self)
        self.pc = 0
        while self.pc < len(self.words):
            w =  self.next_word()
            try:
                w(forth)
            except Exception:
                w.do(forth)
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
        result = f'(SW: {self.name}:'
        for word in self.words:
            result += f' {word}'
        return result + ')'

