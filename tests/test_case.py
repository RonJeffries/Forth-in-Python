from source.forth import Forth
from source.lexicon import Sys


class TestCase:
    def test_hookup(self):
        assert True

    def test_trivial_case(self):
        f = Forth()
        f.process_line(': TEST 3 CASE ENDCASE ;')
        w = f.find_word('TEST')
        words = w.words
        assert str(w) == ': TEST *# 3 DROP ;'

    def test_c_stack_set_up(self):
        f = Forth()
        f.process_line(': TEST 3 CASE GET_C_STACK ENDCASE ;')
        assert f.c_stack.name == 'CASE'
        assert f.c_stack.cells == []

    def test_br_target(self):
        f = Forth()
        test = ': TEST BR_TARGET ;'
        result = f.compile(test)
        result = f.compile('TEST')
        assert (result ==
                'branch not patched in '
                ': TEST BR_TARGET ; ?')

    def test_for_discussion(self):
        f = Forth()
        test = (': TEST'
                '  2 CASE'
                '    1 OF 111 ENDOF'
                '    2 OF 222 ENDOF'
                '  ENDCASE '
                ';')
        expected_stack = [222]
        f.process_line(test)
        w = f.find_word('TEST')
        # assert str(w) == ''

