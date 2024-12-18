import math

from tests.stack import Stack
from tests.word import PrimaryWord, SecondaryWord


class Forth:
    def __init__(self):
        self.stack = Stack()
        self.lexicon = []
        self.define_primaries()

    def define_primaries(self):
        lex = self.lexicon
        stack = self.stack
        lex.append(PrimaryWord('DROP', stack.pop))
        lex.append(PrimaryWord('DUP', stack.dup))
        lex.append(PrimaryWord('OVER', stack.over))
        lex.append(PrimaryWord('ROT', stack.rot))
        lex.append(PrimaryWord('SWAP', stack.swap))
        lex.append(PrimaryWord('+', lambda: stack.push(stack.pop() + stack.pop())))
        lex.append(PrimaryWord('-', lambda: stack.push(-stack.pop() + stack.pop())))
        lex.append(PrimaryWord('*', lambda: stack.push(stack.pop() * stack.pop())))
        lex.append(PrimaryWord('/', lambda: stack.push(1/(stack.pop() / stack.pop()))))
        lex.append(PrimaryWord('SQRT', lambda: stack.push(math.sqrt(stack.pop()))))

    def compile(self, text):
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
