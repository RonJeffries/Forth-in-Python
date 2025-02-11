import pytest

from source.forth import Forth
from source.stack import Stack
from source.word import Word


class TestCompile:

    def test_compiler_hyp(self):
        f = Forth()
        f.process_line(': SQUARE DUP * ;')
        f.process_line(': HYPSQ SQUARE SWAP SQUARE + ;')
        f.process_line(': HYP HYPSQ SQRT ;')
        f.process_line('3 4 HYP')
        assert f.stack.pop() == 5
        assert f.active_words == []

    def test_changing_stack(self):
        f = Forth()
        f.stack = Stack()
        f.stack.extend([3, 4])
        f.find_word('+')(f)
        assert f.stack.pop() == 7

    def test_rot(self):
        forth = Forth()
        forth.stack.extend([0, 1, 2, 3, 4, 5, 6])
        forth.find_word('ROT')(forth)
        assert forth.stack == [0, 1, 2, 3, 5, 6, 4]

    def test_minus(self):
        forth = Forth()
        forth.stack.extend([5, 2])
        forth.find_word('-',)(forth)
        assert forth.stack.pop() == 3

    def test_mod(self):
        forth = Forth()
        forth.stack.extend([192, 128])
        forth.find_word('%')(forth)
        assert forth.stack.pop() == 64
        forth.stack.extend([192, 128])
        forth.find_word('MOD')(forth)
        assert forth.stack.pop() == 64

    def test_divide(self):
        f = Forth()
        f.stack.extend([4, 2])
        f.find_word('/')(f)
        assert f.stack.pop() == 2

    def test_drop(self):
        f = Forth()
        f.stack.extend([4, 2])
        f.find_word('DROP')(f)
        assert f.stack.pop() == 4

    def test_over(self):
        f = Forth()
        f.stack.extend([4, 2])
        f.find_word('OVER')(f)
        assert f.stack == [4, 2, 4]

    def test_syntax_error(self):
        f = Forth()
        s = '; SQUARE DUP + ;'
        with pytest.raises(IndexError) as e:
            f.process_line(s)
        assert (str(e.value) ==
                'pop from empty list')

    def test_undefined_word(self):
        f = Forth()
        s = ': SQUARE UNKNOWN_WORD + ;'
        with pytest.raises(SyntaxError) as e:
            f.process_line(s)
        assert (str(e.value) ==
                'Syntax error: "UNKNOWN_WORD" unrecognized')

    def test_compile_if(self):
        f = Forth()
        s = ': TEST IF DUP + THEN ;'
        f.process_line(s)
        test_word = f.find_word('TEST')
        f.stack.extend([5, 0])
        test_word(f)
        assert f.stack.pop() == 5
        f.stack.extend([5, 1])
        test_word(f)
        assert f.stack.pop() == 10

    def test_lit_hand_compiled(self):
        f = Forth()
        # s = ': 3 DUP +'
        lit = f.find_word('*#')
        dup = f.find_word('DUP')
        plus = f.find_word('+')
        indices = [lit, 3, dup, plus]
        sw = Word('TEST', indices)
        sw(f)
        assert f.stack.pop() == 6

    def test_lit_compiled(self):
        f = Forth()
        f.process_line('3 4 +')
        assert f.stack.pop() == 7

    def test_if_true(self):
        f = Forth()
        s = ': TEST 5 1 IF DUP + THEN 100 + ;'
        f.process_line(s)
        test_word = f.find_word('TEST')
        test_word(f)
        assert f.stack.pop() == 110

    def test_if_false(self):
        f = Forth()
        s = ': TEST 5 0 IF DUP + THEN 100 + ;'
        f.process_line(s)
        test_word = f.find_word('TEST')
        test_word(f)
        assert f.stack.pop() == 105

    def test_if_nested(self):
        f = Forth()
        s = ': TEST 200 100 1 1 IF 5 SWAP IF DUP THEN THEN + ;'
        f.process_line(s)
        test_word = f.find_word('TEST')
        test_word(f)
        assert f.stack.pop() == 10
        assert f.stack == [200, 100]

        f = Forth()
        s = ': TEST 200 100 0 1 IF 5 SWAP IF DUP THEN THEN + ;'
        f.process_line(s)
        test_word = f.find_word('TEST')
        test_word(f)
        assert f.stack.pop() == 105

        f = Forth()
        s = ': TEST 200 100 0 IF 5 SWAP IF DUP THEN THEN + ;'
        f.process_line(s)
        test_word = f.find_word('TEST')
        test_word(f)
        assert f.stack.pop() == 300

    def test_else(self):
        f = Forth()
        s = ': TEST IF 5 ELSE 50 THEN ;'
        f.process_line(s)
        test_word = f.find_word('TEST')
        f.stack.push(1)
        test_word(f)
        assert f.stack.pop() == 5
        f.stack.push(0)
        test_word(f)
        assert f.stack.pop() == 50

    def test_conditionals(self):
        f = Forth()
        f.process_line(' 1 1 = ')
        assert f.stack.pop() == f.true
        f.process_line(' 2 1 = ')
        assert f.stack.pop() == f.false
        f.process_line(' 2 1 < ')
        assert f.stack.pop() == f.true
        f.process_line(' 1 2 < ')
        assert f.stack.pop() == f.false
        f.process_line(' 2 1 > ')
        assert f.stack.pop() == f.false
        f.process_line(' 1 2 > ')
        assert f.stack.pop() == f.true
        f.process_line(' 2 1 >= ')
        assert f.stack.pop() == f.false
        f.process_line(' 1 2 >= ')
        assert f.stack.pop() == f.true
        f.process_line(' 2 2 >= ')
        assert f.stack.pop() == f.true
        f.process_line(' 2 1 <= ')
        assert f.stack.pop() == f.true
        f.process_line(' 1 2 <= ')
        assert f.stack.pop() == f.false
        f.process_line(' 2 2 <= ')
        assert f.stack.pop() == f.true

    def test_double(self):
        f = Forth()
        s = ': DOUBLE 2 * ;'
        f.process_line(s)
        s = ': TEST 5 DOUBLE DOUBLE DOUBLE ;'
        f.process_line(s)
        f.process_line('TEST')
        assert f.stack.pop() == 40

    def test_double_under(self):
        f = Forth()
        f.process_line(': DOUBLE 2 * ;')
        f.process_line(': DU SWAP DOUBLE SWAP ;')
        s = ': TEST 2 5 DU DU DU DU ;'
        f.process_line(s)
        test = f.find_word('TEST')
        test(f)
        assert f.stack.pop() == 5
        assert f.stack.pop() == 32

    def test_double_under_direct(self):
        f = Forth()
        f.process_line(': DOUBLE 2 * ;')
        f.process_line(': DU SWAP DOUBLE SWAP ;')
        s = ' 2 5 DU DU DU DU '
        f.process_line(s)
        assert f.stack.pop() == 5
        assert f.stack.pop() == 32

    def test_begin_until_hard(self):
        f = Forth()
        f.process_line(': DOUBLE 2 * ;')
        f.process_line(': DOUBLE_UNDER SWAP DOUBLE SWAP ;')
        s = ': TEST 2 5 BEGIN DOUBLE_UNDER 1- DUP 0 >= UNTIL ;'
        f.process_line(s)
        f.process_line('TEST')
        assert f.stack.pop() == 0
        assert f.stack.pop() == 64

    @pytest.mark.skip('revise for new compiler state')
    def test_begin_until_inline(self):
        f = Forth()
        s = ' 2 5 BEGIN SWAP 2 * SWAP 1- DUP 0 >= UNTIL '
        f.process_line(s)
        assert f.stack.pop() == 0
        assert f.stack.pop() == 64

    def test_pow_step(self):
        f = Forth()
        pow_step = ': POW_STEP DUP ROT * SWAP ;'
        f.process_line(pow_step)
        f.process_line(' 9 3 POW_STEP ')
        assert f.stack.pop() == 3
        assert f.stack.pop() == 27

    def test_power(self):
        f = Forth()
        f.process_line(': 2ROT ROT ROT ;')
        pow_step = (': POW_STEP '
                    '(prod base -- prod*base base)'
                    'DUP ROT * SWAP ;')
        f.process_line(pow_step)
        f.process_line(': POWER'
                  '(base power -- base**power) '
                  '1 2ROT           (1 base power)'
                  'BEGIN 2ROT       (power 1 base)'
                  'POW_STEP         (power product base)'
                  'ROT              (product base power)'
                  '1- DUP 0 = UNTIL (product base power)'
                  'DROP DROP        (product) ;')
        f.process_line(' 3 4 POWER ')
        assert f.stack.pop() == 81

    def test_comment(self):
        f = Forth()
        f.process_line(': TEST ( a b -- b a ) SWAP ;')
        f.process_line(': TEST (a b -- b a) SWAP ;')

    def test_different_loop(self):
        p = (': POWER'
             '(base power -- base**power) '
             '1 2ROT (1 base power)'
             'DO_N POW_STEP LOOP DROP ;')

    def test_return_stack(self):
        f = Forth()
        s = ' 3 >R 4 5 + R@ + R> +'
        f.process_line(s)
        assert f.return_stack == []
        assert f.stack.pop() == 15

    @pytest.mark.skip('revise for new compiler state')
    def test_initial_do(self):
        f = Forth()
        s = ' 5 0 DO I 10 * LOOP '
        f.process_line(s)
        assert f.stack.stack == [0, 10, 20, 30, 40]

    def test_direct_execute(self):
        f = Forth()
        f.process_line('3 4')
        assert f.stack.stack == [3, 4]

    def test_direct_harder(self):
        f = Forth()
        s = (': SUM + ; '
             ' 3 4 SUM')
        f.process_line(s)
        assert f.stack.pop() == 7

    def test_2DUP(self):
        f = Forth()
        s = '1 5 2DUP'
        f.process_line(s)
        assert f.stack.stack == [1, 5, 1, 5]

    @pytest.mark.skip('revise for new compiler state')
    def test_compiled_star_loop(self):
        f = Forth()
        f.process_line(': JUMP_BACK ;')
        f.process_line(': SKIP ;')
        star_loop = ': *LOOP R> R> SWAP 1 + 2DUP < IF SWAP >R >R JUMP_BACK ELSE DROP DROP SKIP THEN ;'
        # f.compile(star_loop)
        s = ' 5 0 DO I 10 * LOOP '
        f.process_line(s)
        assert f.stack.stack == [0, 10, 20, 30, 40]

    def test_rudimentary_heap(self):
        f = Forth()
        f.process_line('9 ALLOT')
        f.process_line('666 4 !')
        assert f.heap.at(4) == 666
        f.process_line('4 @')
        assert f.stack.pop() == 666

    def test_rudimentary_heap_arithmetic(self):
        f = Forth()
        f.process_line('9 ALLOT')
        f.process_line('666 4 !')
        f.process_line('1 3 + @')
        assert f.stack.pop() == 666

    def test_rudimentary_heap_overflow(self):
        f = Forth()
        with pytest.raises(IndexError):
            f.process_line('666 10 !')


    def test_constant(self):
        f = Forth()
        f.process_line('666 CONSTANT FOO')
        f.process_line('777 CONSTANT BAR')
        f.process_line('888 CONSTANT BAZ')
        assert f.stack.stack == []
        f.process_line('BAZ BAR FOO')
        assert f.stack.stack == [888, 777, 666]

    def test_variable(self):
        f = Forth()
        f.process_line('VARIABLE FOO 1 ALLOT')
        f.process_line('VARIABLE BAR 1 ALLOT')
        f.process_line('VARIABLE BAZ 1 ALLOT')
        f.process_line('666 FOO !')
        f.process_line('777 BAR !')
        f.process_line('888 BAZ !')
        f.process_line('BAZ @ BAR @ FOO @')
        assert f.stack.stack == [888, 777, 666]

    def test_variable_without_allot_fails(self):
        f = Forth()
        f.process_line('VARIABLE FOO')
        with pytest.raises(IndexError):
            f.process_line('FOO @')

    def test_compile_create_does(self):
        f = Forth()
        f.process_line('1 , 2 , 3 ,')
        s = ': CONSTANT CREATE , DOES> @ ;'
        f.process_line(s)
        expected = f.heap.next_available()
        f.process_line('2025 CONSTANT YEAR')
        assert f.heap.at(expected) == 2025
        f. process_line('YEAR')
        assert f.stack.flush() == [2025]

    def test_compile_two_constants(self):
        f = Forth()
        f.process_line('1 , 2 , 3 ,')
        s = ': CONSTANT CREATE , DOES> @ ;'
        f.process_line(s)
        f.process_line('2025 CONSTANT YEAR')
        f.process_line('1939 CONSTANT BIRTH_YEAR')
        f. process_line('YEAR BIRTH_YEAR - 1 -')
        assert f.stack.flush() == [85]

    def test_create_makes_a_word(self):
        f = Forth()
        f.process_line('CREATE FOO')
        f. process_line('FOO')

    def test_first_create_is_at_zero(self):
        f = Forth()
        f.process_line('CREATE FOO')
        f. process_line('FOO')
        assert f.stack.flush() == [0]

    def test_create_is_at_heap_end(self):
        f = Forth()
        f.process_line('VARIABLE FOO 3 ALLOT')
        assert f.heap.next_available() == 3
        f.process_line('CREATE BAR')
        f. process_line('BAR')
        assert f.stack.flush() == [3]

    def test_demo_create(self):
        f = Forth()
        f.process_line('VARIABLE FOO 3 ALLOT')
        assert f.heap.next_available() == 3
        f.process_line('CREATE BAR 1 ALLOT')
        f. process_line('BAR @')
        assert f.stack.flush() == [0]
        f.process_line('42 BAR !')
        assert f.stack.stack == []
        f. process_line('BAR @')
        assert f.stack.flush() == [42]

    def test_comma(self):
        f = Forth()
        assert f.heap.next_available() == 0
        f.process_line('33 ,')
        assert f.heap.next_available() == 1
        assert f.heap.at(0) == 33

    def test_create_comma(self):
        f = Forth()
        f.process_line('CREATE BAR 19 , BAR @  23 +')
        assert f.stack.flush() == [42]

    def test_get_lexicon_info(self):
        f = Forth()
        print(len(f.lexicon.lexicon))
        words = sorted([w.name for w in f.lexicon.lexicon])
        print(" ".join(words))

    def test_destroy_world(self):
        f = Forth()
        f.process_line(': EXECUTE BEGIN 666 0 UNTIL ;')
        with pytest.raises(ValueError) as e:
            f.process_line(' EXECUTE ')
        assert str(e.value) == 'Stack is full'

    def test_partial_definition(self):
        f = Forth()
        with pytest.raises(ValueError) as e:
            f.process_line(': FOO 444 222 +')
        assert str(e.value) == 'Unexpected end of input'

    def test_safe_compile(self):
        f = Forth()
        result = f.compile('1 2 3 2 /')
        assert result == "ok"
        result = f.compile('1 2 3 0 /')
        assert result == 'integer division or modulo by zero ?'
        assert f.stack.is_empty()

    def test_safe_compile_needs_more_input(self):
        f = Forth()
        result = f.compile(': FOO 42 ')  # no semicolon
        assert result == '...'

    def test_repr(self):
        f = Forth()
        f.compile(': double dup + ;')
        w = f.find_word('DOUBLE')
        assert repr(w) == ': DOUBLE DUP + ;'
        f.compile(': QUAD double double ;')
        w = f.find_word('QUAD')
        assert repr(w) == ': QUAD DOUBLE DOUBLE ;'
        w = f.find_word('DUP')
        assert repr(w) == 'DUP'

    def test_clears_compilation_state(self):
        f = Forth()
        msg = f.compile(': foo bar ;')
        assert msg == 'Syntax error: "BAR" unrecognized ?'
        assert f.compilation_state == False

    # def test_repr_if(self):
    #     f = Forth()
    #     f.compile(': FOO 1 IF 255 ELSE 127 THEN ;')
    #     w = f.find_word('FOO')
    #     assert repr(w) == 'FOO'

    def test_minus_1(self):
        i = 0xFFFFFFFF
        j = i ^ 0x80000000
        k = 0x00000000
        print(f'{hex(i)} {hex(j)} {hex(k)}')
        # assert False

    def test_or(self):
        f = Forth()
        f.compile('0 0 or')
        assert f.stack.flush() == [f.false]
        f.compile('-1 0 or')
        assert f.stack.flush() == [f.true]
        f.compile('0 -1 or')
        assert f.stack.flush() == [f.true]
        f.compile('-1 -1 or')
        assert f.stack.flush() == [f.true]

    def test_and(self):
        f = Forth()
        f.compile('0 0 and')
        assert f.stack.flush() == [f.false]
        f.compile('-1 0 and')
        assert f.stack.flush() == [f.false]
        f.compile('0 -1 and')
        assert f.stack.flush() == [f.false]
        f.compile('-1 -1 and')
        assert f.stack.flush() == [f.true]

    def test_invert(self):
        f = Forth()
        f.compile('1 1 = invert')
        assert f.stack.flush() == [f.false]
        f.compile('0 1 = invert')
        assert f.stack.flush() == [f.true]

    def test_and_or_invert_on_integers(self):
        f = Forth()
        f.compile('7 2 and')
        assert f.stack.flush() == [2]
        f.compile('3 7 and')
        assert f.stack.flush() == [3]
        f.compile('2 5 or')
        assert f.stack.flush() == [7]
        f.compile(' 2 2 = invert')
        assert f.stack.flush() == [f.false]
        f.compile(' 2 3 = invert')
        assert f.stack.flush() == [f.true]
