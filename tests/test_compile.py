import pytest

from tests.forth import Forth
from tests.stack import Stack
from tests.word import SecondaryWord


class TestCompile:

    def test_compiler_hyp(self):
        f = Forth()
        f.compile(': SQUARE DUP * ;')
        f.compile(': HYPSQ SQUARE SWAP SQUARE + ;')
        hyp = f.compile(': HYP HYPSQ SQRT ;')
        f.stack.extend([3, 4])
        hyp.do(f)
        assert f.stack.pop() == 5
        assert f.active_words == []

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
        s = ': SQUARE UNKNOWN_WORD + ;'
        with pytest.raises(SyntaxError) as e:
            f.compile(s)
        assert str(e.value) == 'Syntax error: "UNKNOWN_WORD" unrecognized'

    @pytest.mark.skip(reason='not implemented')
    def test_star_if(self):
        f = Forth()
        s = ': TEST *IF DUP + ;'
        test_word = f.compile(s)
        star_if = f.find_word('*IF')
        star_if.parameter = 2
        f.stack.extend([2, 0])
        test_word.do(f)
        assert f.stack.pop() == 2
        f.stack.extend([2, 1])
        test_word.do(f)
        assert f.stack.pop() == 4

    @pytest.mark.skip(reason='not implemented')
    def test_compile_if(self):
        f = Forth()
        s = ': TEST IF DUP + ;'
        test_word = f.compile(s)
        assert test_word.words[0] == 0

    def test_lit_hand_compiled(self):
        f = Forth()
        # s = ': 3 DUP +'
        lit = f.find_word('*#')
        dup = f.find_word('DUP')
        plus = f.find_word('+')
        indices = [lit, 3, dup, plus]
        sw = SecondaryWord('TEST', indices)
        sw.do(f)
        assert f.stack.pop() == 6

    def test_lit_compiled(self):
        f = Forth()
        f.compile(': TEST 3 4 + ;').do(f)
        assert f.stack.pop() == 7




