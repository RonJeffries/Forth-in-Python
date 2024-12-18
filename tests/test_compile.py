import math

import pytest

from forth import stack, lexicon
from tests.test_first_classes import PrimaryWord, SecondaryWord, clear

def forth_compile(text, lex):
    words = text.split()
    match words:
        case ':', defining, *rest, ';':
            word_list = [ix for word in rest if (ix := find_word_index(word, lex)) is not None]
            lex.append(SecondaryWord(defining, word_list))
        case _:
            raise SyntaxError(f'Syntax error: "{text}". Missing : or ;?')

def find_word_index(word, lex):
    for i in range(len(lex)):
        if lex[i].name == word:
            return i
    raise ValueError(f'cannot find word "{word}"')

def find_word(word, lex):
    return lex[find_word_index(word, lex)]


class TestCompile:

    def test_compiler_hyp(self):
        clear()
        lexicon.append(PrimaryWord('+', lambda: stack.append(stack.pop() + stack.pop())))
        lexicon.append(PrimaryWord('-', lambda: stack.append(stack.pop() - stack.pop())))
        lexicon.append(PrimaryWord('*', lambda: stack.append(stack.pop() * stack.pop())))
        lexicon.append(PrimaryWord('DUP', lambda: stack.append(stack[-1])))
        lexicon.append(PrimaryWord('SWAP', lambda: stack.extend([stack.pop(), stack.pop()])))
        lexicon.append(PrimaryWord('SQRT', lambda: stack.append(math.sqrt(stack.pop()))))
        forth_compile(': SQUARE DUP * ;', lexicon)
        forth_compile(': HYPSQ SQUARE SWAP SQUARE + ;', lexicon)
        forth_compile(': HYP HYPSQ SQRT ;', lexicon)
        stack.extend([3, 4])
        find_word('HYP', lexicon).do(lexicon)
        assert stack.pop() == 5

    def test_syntax_error(self):
        s = '; SQUARE DUP + ;'
        with pytest.raises(SyntaxError) as e:
            forth_compile(s, lexicon)
        assert str(e.value) == 'Syntax error: "; SQUARE DUP + ;". Missing : or ;?'

    def test_undefined_word(self):
        s = ': SQUARE DUMB + ;'
        with pytest.raises(ValueError) as e:
            forth_compile(s, lexicon)
        assert str(e.value) == 'cannot find word "DUMB"'



