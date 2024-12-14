import math

import pytest

stack = []

def clear():
    global stack
    stack = []

def plus():
    # ( x1 x2 -- x1+x2 )
    x2, x1 = stack.pop(), stack.pop()
    stack.append(x1 + x2)

def number(n):
    stack.append(n)

def interpret(s):
    print(f'interpret {s}')
    words = s.split()
    for word in words:
        interpret_word(word)

def interpret_word(word):
    print(f'word {word}')
    if is_number(word):
        stack.append(int(word))
    elif word == '+':
        plus()
    elif word == '-':
        # ( x1 x2 == x1 - x2
        x2, x1 = stack.pop(), stack.pop()
        stack.append(x1 - x2)
    elif word == '*':
        x2, x1 = stack.pop(), stack.pop()
        stack.append(x1 * x2)
    elif word == 'SQRT':
        stack.append(math.sqrt(stack.pop()))
    elif word == 'SWAP':
        # ( x1 x2 -- x2 x1 )
        x2, x1 = stack.pop(), stack.pop()
        stack.append(x2); stack.append(x1)
    elif word == 'DUP':
        x1 = stack.pop()
        stack.append(x1); stack.append(x1)
    elif word == 'NEGATE':
        s = '0 SWAP -'
        interpret(s)
    elif word == 'SQUARE':
        interpret('DUP *')
    elif word == 'HYPOTENUSE':
        s = 'SQUARE SWAP SQUARE + SQRT'
        interpret(s)
    else:
        raise ValueError(f'Invalid word {word}')

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class TestInitial:
    def test_stack_plus(self):
        clear()
        number(3)
        number(4)
        plus()
        assert stack.pop() == 7

    def test_stack_insufficient(self):
        clear()
        number(3)
        with pytest.raises(IndexError):
            plus()
        assert len(stack) == 0

    def test_interpret_string(self):
        clear()
        s = '3 4 +'
        interpret(s)
        assert stack.pop() == 7

    def test_minus(self):
        clear()
        s = '100 49 -'
        interpret(s)
        assert stack.pop() == 51

    def test_swap(self):
        clear()
        s = '1 2 SWAP'
        interpret(s)
        assert stack.pop() == 1
        assert stack.pop() == 2

    def test_dup(self):
        clear()
        s = '100 DUP'
        interpret(s)
        assert stack.pop() == 100
        assert stack.pop() == 100

    def test_times(self):
        clear()
        s = '5 6 *'
        interpret(s)
        assert stack.pop() == 30

    def test_negate(self):
        clear()
        s = '100 NEGATE'
        interpret(s)
        assert stack.pop() == -100

    def test_square(self):
        clear()
        s = '10 SQUARE'
        interpret(s)
        assert stack.pop() == 100

    def test_sqrt(self):
        clear()
        s = '4 SQRT'
        interpret(s)
        assert stack.pop() == 2

    def test_hyp(self):
        clear()
        s = '3 4 HYPOTENUSE'
        interpret(s)
        assert stack.pop() == 5
        assert False
