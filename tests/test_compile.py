import pytest

from tests.forth import Forth
from tests.stack import Stack


class TestCompile:

    def test_compiler_hyp(self):
        f = Forth()
        f.compile(': SQUARE DUP * ;')
        f.compile(': HYPSQ SQUARE SWAP SQUARE + ;')
        f.compile(': HYP HYPSQ SQRT ;')
        f.stack.extend([3, 4])
        f.find_word('HYP').do(f)
        assert f.stack.pop() == 5

    def test_changing_stack(self):
        f = Forth()
        f.stack = Stack()
        f.stack.extend([3, 4])
        f.find_word('+').do(f)
        assert f.stack.pop() == 7

    def test_rot(self):
        forth = Forth()
        forth.stack.extend([0, 1, 2, 3, 4, 5, 6])
        forth.find_word('ROT').do(forth)
        assert forth.stack == [0, 1, 2, 3, 5, 6, 4]

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



