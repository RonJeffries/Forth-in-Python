import math

from tests.stack import Stack
from tests.word import PrimaryWord, SecondaryWord


class Forth:
    def __init__(self):
        self.stack = Stack()
        self.lexicon = []
        self.define_primaries()
        self.active_words = []

    @property
    def active_word(self):
        return self.active_words[-1]

    def begin(self, word):
        self.active_words.append(word)

    def end(self):
        self.active_words.pop()

    def next_word(self):
        return self.active_word.next_word()

    def define_primaries(self):
        lex = self.lexicon
        lex.append(PrimaryWord('*#', lambda f: f.stack.push(f.next_word())))
        lex.append(PrimaryWord('DROP', lambda f: f.stack.pop()))
        lex.append(PrimaryWord('DUP', lambda f: f.stack.dup()))
        lex.append(PrimaryWord('OVER', lambda f: f.stack.over()))
        lex.append(PrimaryWord('ROT', lambda f: f.stack.rot()))
        lex.append(PrimaryWord('SWAP', lambda f: f.stack.swap()))
        lex.append(PrimaryWord('+', lambda f: f.stack.push(f.stack.pop() + f.stack.pop())))
        lex.append(PrimaryWord('-', lambda f: f.stack.push(f.stack.swap_pop() - f.stack.pop())))
        lex.append(PrimaryWord('*', lambda f: f.stack.push(f.stack.pop() * f.stack.pop())))
        lex.append(PrimaryWord('/', lambda f: f.stack.push(f.stack.swap_pop() / f.stack.pop())))
        lex.append(PrimaryWord('SQRT', lambda f: f.stack.push(math.sqrt(f.stack.pop()))))

    def compile(self, text):
        # why don't we just store the word in the list, it's no larger than the index
        words = text.split()
        match words:
            case ':', defining, *rest, ';':
                word_list = [ix for word in rest if (ix := self.find_word_index(word)) is not None]
                self.lexicon.append(SecondaryWord(defining, word_list))
            case _:
                raise SyntaxError(f'Syntax error: "{text}". Missing : or ;?')

    def find_word_index(self, word):
        lex = self.lexicon
        for i in range(len(lex)):
            if lex[i].name == word:
                return i
        raise ValueError(f'cannot find word "{word}"')

    def find_word(self, word):
        return self.lexicon[self.find_word_index(word)]
