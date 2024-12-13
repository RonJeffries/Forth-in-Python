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
    words = s.split()
    for word in words:
        interpret_word(word)

def interpret_word(word):
    if is_number(word):
        stack.append(int(word))
    elif word == '+':
        plus()
    elif word == '-':
        # ( x1 x2 == x1 - x2
        x2, x1 = stack.pop(), stack.pop()
        stack.append(x1 - x2)
def interpret_word(word):
    if is_number(word):
        stack.append(int(word))
    elif word == '+':
        plus()
    elif word == '-':
        # ( x1 x2 == x1 - x2
        x2, x1 = stack.pop(), stack.pop()
        stack.append(x1 - x2)

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
