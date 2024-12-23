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
                word_list = self.compile_word_list(rest)
                word = SecondaryWord(defining, word_list)
                self.lexicon.append(word)
                return word
            case _:
                raise SyntaxError(f'Syntax error: "{text}". Missing : or ;?')

    def compile_word_list(self, rest):
        word_list = []
        for word in rest:
            if (definition := self.find_word(word)) is not None:
                word_list.append(definition)
            elif (num := self.compile_number(word)) is not None:
                definition = self.find_word('*#')
                word_list.append(definition)
                word_list.append(num)
            else:
                raise SyntaxError(f'Syntax error: "{word}" unrecognized')
        return word_list

    def compile_number(self, word):
        try:
            num = int(word)
            return num
        except ValueError:
            return None

    def find_word(self, word):
        for definition in self.lexicon:
            if definition.name == word:
                return definition
        return None
