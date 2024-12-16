import math

stack = []
lexicon = []

def clear():
    global stack, lexicon
    stack = []
    lexicon = []


class PrimaryWord:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return f'PW: {self.name}'

    def do(self):
        self.code()

class SecondaryWord:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return f'SW: {self.name}'

    def do(self):
        for word_index in self.code:
            word = lexicon[word_index]
            word.do()


class TestFirstClasses:
    def test_hookup(self):
        assert True

    def test_first_word(self):
        word = PrimaryWord('+', lambda: stack.append(stack.pop() + stack.pop()))
        stack.append(1)
        stack.append(3)
        word.do()
        assert stack.pop() == 4

    def test_double(self):
        w0 = PrimaryWord('+', lambda: stack.append(stack.pop() + stack.pop()))
        w1 = PrimaryWord('DUP', lambda: stack.append(stack[-1]))
        lexicon.append(w0)
        lexicon.append(w1)
        s0 = SecondaryWord('DOUBLE', [1, 0])
        stack.append(2)
        s0.do()
        assert stack.pop() == 4

    def test_hypotenuse(self):
        clear()
        w_plus = PrimaryWord('+', lambda: stack.append(stack.pop() + stack.pop()))
        w_dup = PrimaryWord('DUP', lambda: stack.append(stack[-1]))
        w_swap = PrimaryWord('SWAP', lambda: stack.extend([stack.pop(), stack.pop()]))
        w_times = PrimaryWord('*', lambda: stack.append(stack.pop() * stack.pop()))
        w_sqrt = PrimaryWord('SQRT', lambda: stack.append(math.sqrt(stack.pop())))
        w_square = SecondaryWord('SQUARE', [1, 3])
        w_hypsq = SecondaryWord('HYPSQ', [5, 2, 5, 0])
        w_hyp = SecondaryWord('HYP', [6, 4])
        lexicon.extend([w_plus, w_dup, w_swap, w_times, w_sqrt, w_square, w_hypsq, w_hyp])
        #               0       1      2       3        4       5         6        7
        stack.append(3)
        stack.append(4)
        w_hyp.do()
        assert stack.pop() == 5


