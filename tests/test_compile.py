import math

import pytest

from forth import stack, lexicon
from tests.test_first_classes import PrimaryWord, SecondaryWord, clear

def forth_compile(text, lex):
    words = text.split()
    match words:
        case ':', defining, *rest, ';':
            word_list = [ix for word in rest if (ix := find_word(word, lex)) is not None]
            lex.append(SecondaryWord(defining, word_list))
        case _:
            raise SyntaxError(f'Syntax error: "{text}". Missing : or ;?')

def find_word(word, lex):
    for i in range(len(lex)):
        if lex[i].name == word:
            return i
    raise ValueError(f'cannot find word "{word}"')


class TestCompile:

    def test_compiler_hyp(self):
        clear()
        w_plus = PrimaryWord('+', lambda: stack.append(stack.pop() + stack.pop()))
        w_dup = PrimaryWord('DUP', lambda: stack.append(stack[-1]))
        w_swap = PrimaryWord('SWAP', lambda: stack.extend([stack.pop(), stack.pop()]))
        w_times = PrimaryWord('*', lambda: stack.append(stack.pop() * stack.pop()))
        w_sqrt = PrimaryWord('SQRT', lambda: stack.append(math.sqrt(stack.pop())))
        lexicon.extend([w_plus, w_dup, w_swap, w_times, w_sqrt])
        print(f'tc lex {lexicon}')
        s = ': SQUARE DUP * ;'
        forth_compile(s, lexicon)
        index = find_word('SQUARE', lexicon)
        word = lexicon[index]
        assert word.name == 'SQUARE'
        assert word.code == [1, 3]
        hypsq = ': HYPSQ SQUARE SWAP SQUARE + ;'
        forth_compile(hypsq, lexicon)
        hyp = ': HYP HYPSQ SQRT ;'
        forth_compile(hyp, lexicon)
        index = find_word('HYP', lexicon)
        word = lexicon[index]
        stack.extend([3, 4])
        word.do(lexicon)
        print(f'{stack=}')
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



