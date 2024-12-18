import math
import pytest

from tests.word import PrimaryWord, SecondaryWord

class Forth:
    def __init__(self):
        self.stack = []
        self.lexicon = []
        self.define_primaries()

    def define_primaries(self):
        lex = self.lexicon
        stack = self.stack
        lex.append(PrimaryWord('+', lambda: stack.append(stack.pop() + stack.pop())))
        lex.append(PrimaryWord('-', lambda: stack.append(-stack.pop() + stack.pop())))
        lex.append(PrimaryWord('*', lambda: stack.append(stack.pop() * stack.pop())))
        lex.append(PrimaryWord('/', lambda: stack.append(1/(stack.pop() / stack.pop()))))
        lex.append(PrimaryWord('DUP', lambda: stack.append(stack[-1])))
        lex.append(PrimaryWord('DROP', lambda: stack.pop()))
        lex.append(PrimaryWord('OVER', lambda: stack.append(stack[-2])))
        lex.append(PrimaryWord('SWAP', lambda: stack.extend([stack.pop(), stack.pop()])))
        lex.append(PrimaryWord('SQRT', lambda: stack.append(math.sqrt(stack.pop()))))

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


class TestCompile:

    def test_compiler_hyp(self):
        f = Forth()
        f.compile(': SQUARE DUP * ;')
        f.compile(': HYPSQ SQUARE SWAP SQUARE + ;')
        f.compile(': HYP HYPSQ SQRT ;')
        f.stack.extend([3, 4])
        f.find_word('HYP').do(f)
        assert f.stack.pop() == 5

    def test_minus(self):
        forth = Forth()
        forth.stack.extend([5, 2])
        forth.find_word('-',).do(forth)
        assert forth.stack.pop() == 3

    def test_divide(self):
        f = Forth()
        f.stack.extend([4, 2])
        f.find_word('/').do(f)
        assert f.stack.pop() == 2

    def test_drop(self):
        f = Forth()
        f.stack.extend([4, 2])
        f.find_word('DROP').do(f)
        assert f.stack.pop() == 4

    def test_over(self):
        f = Forth()
        f.stack.extend([4, 2])
        f.find_word('OVER').do(f)
        assert f.stack == [4, 2, 4]

    def test_syntax_error(self):
        f = Forth()
        s = '; SQUARE DUP + ;'
        with pytest.raises(SyntaxError) as e:
            f.compile(s)
        assert str(e.value) == 'Syntax error: "; SQUARE DUP + ;". Missing : or ;?'

    def test_undefined_word(self):
        f = Forth()
        s = ': SQUARE DUMB + ;'
        with pytest.raises(ValueError) as e:
            f.compile(s)
        assert str(e.value) == 'cannot find word "DUMB"'



