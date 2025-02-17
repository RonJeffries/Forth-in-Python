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
        expected = (
            ': TEST *# 2 *# 1 OVER = 0BR 10 '
            'DROP *# 111 BR BR_TARGET *# 2 OVER = 0BR 19 '
            'DROP *# 222 BR BR_TARGET DROP ;')
        assert str(w) == expected

    def test_pattern(self):
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
        branch_location = w.index('0BR') + 1
        # branch_location = 4 + 1
        target_location = w.index('0BR', branch_location) - 3
        # target_location = 13 - 3
        assert w.words[branch_location] == target_location

