from source.forth import Forth


class TestCase:
    def test_hookup(self):
        assert True

    def test_trivial_case(self):
        f = Forth()
        f.compile(': TEST 3 CASE ENDCASE ;')
        w = f.find_word('TEST')
        words = w.words
        assert str(w) == ': TEST _# 3 DROP ;'

    def test_c_stack_set_up(self):
        f = Forth()
        f.compile(': TEST 3 CASE _PEEK_CS ENDCASE ;')
        assert f.c_stack_top.name == 'CASE'
        assert f.c_stack_top.locations == []

    def test_br_target(self):
        f = Forth()
        test = ': TEST _BR_TGT ;'
        result = f.compile(test)
        result = f.compile('TEST')
        assert (result ==
                'branch not patched in '
                ': TEST _BR_TGT ; ?')

    def test_for_discussion(self):
        f = Forth()
        test = (': TEST'
                '  2 CASE'
                '    1 OF 111 ENDOF'
                '    2 OF 222 ENDOF'
                '  ENDCASE '
                ';')
        expected_stack = [222]
        f.compile(test)
        w = f.find_word('TEST')
        expected = (
            ': TEST _# 2 _# 1 OVER = _0BR 10 '
            'DROP _# 111 _BR 20 _# 2 OVER = _0BR 19 '
            'DROP _# 222 _BR 20 DROP ;')
        assert str(w) == expected

    def test_pattern_of_cases(self):
        f = Forth()
        test = (': TEST'
                '  2 CASE'
                '    1 OF 111 ENDOF'
                '    2 OF 222 ENDOF'
                '  ENDCASE '
                ';')
        expected_stack = [222]
        f.compile(test)
        w = f.find_word('TEST')
        branch_location = w.index('_0BR') + 1
        # branch_location = 4 + 1
        target_location = w.index('_0BR', branch_location) - 3
        # target_location = 13 - 3
        assert w.words[branch_location] == target_location

    def test_pattern_exits(self):
        f = Forth()
        test = (': TEST'
                '  2 CASE'
                '    1 OF 111 ENDOF'
                '    2 OF 222 ENDOF'
                '  ENDCASE '
                ';')
        expected_stack = [222]
        f.compile(test)
        w = f.find_word('TEST')
        first_exit_location = w.index('_BR') + 1
        assert w.words[first_exit_location] == 20
        second_exit_location = w.index('_BR', first_exit_location) + 1
        assert w.words[second_exit_location] == 20

    def test_branch(self):
        f = Forth()
        test = ': TEST 5 _BR _BR_TGT DUP + 3 + ;'
        #              0 1  2         3   4 5 6
        ok = f.compile(test)
        assert ok == 'ok'
        w = f.find_word('TEST')
        words = w.words
        assert words[2] == f.find_word('_BR_TGT')
        words[2] = 5
        f.compile('TEST')
        assert f.stack.pop() == 8

    def test_zero_branch_branches(self):
        f = Forth()
        test = ': TEST 5 0 _0BR _BR_TGT DUP + 3 + ;'
        #              0 1  2  3         4   5 6 7
        ok = f.compile(test)
        assert ok == 'ok'
        w = f.find_word('TEST')
        words = w.words
        assert words[3] == f.find_word('_BR_TGT')
        words[3] = 6
        f.compile('TEST')
        assert f.stack.pop() == 8

    def test_zero_branch_no_branch(self):
        f = Forth()
        test = ': TEST 5 1 _0BR _BR_TGT DUP + 3 + ;'
        #              0 1  2  3         4   5 6 7
        ok = f.compile(test)
        assert ok == 'ok'
        w = f.find_word('TEST')
        words = w.words
        assert words[3] == f.find_word('_BR_TGT')
        words[3] = 6
        f.compile('TEST')
        assert f.stack.pop() == 13

    def test_famous_case_behavior(self):
        f = Forth()
        case = ': T CASE 1 OF 111 ENDOF 2 OF 222 ENDOF ENDCASE ;'
        f.compile(case)
        assert f.stack.is_empty()
        f.compile(' 1 T')
        assert f.stack.pop() == 111
        assert f.stack.is_empty()
        f.compile(' 2 T')
        assert f.stack.pop() == 222
        assert f.stack.is_empty()
        f.compile(' 3 T')
        assert f.stack.is_empty()

    def test_famous_case_behavior_default(self):
        f = Forth()
        case = ': T CASE 1 OF 111 ENDOF 2 OF 222 ENDOF >R 666 R> ENDCASE ;'
        f.compile(case)
        assert f.stack.is_empty()
        f.compile(' 1 T')
        assert f.stack.pop() == 111
        assert f.stack.is_empty()
        f.compile(' 2 T')
        assert f.stack.pop() == 222
        assert f.stack.is_empty()
        f.compile(' 3 T')
        assert f.stack.pop() == 666

