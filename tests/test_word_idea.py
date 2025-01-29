

stack = []

class Word:
    def __init__(self):
        self.code = []

    def append(self, func):
        self.code.append(func)

    def do(self):
        for f in self.code:
            f()


class TestWordIdea:
    def init(self):
        global stack
        stack = []

    def test_hookup(self):
        assert True

    def test_primary_word(self):
        self.init()
        stack.append(2)
        word = Word()
        word.append(lambda: stack.append(stack.pop() * 2))
        word.do()
        assert stack.pop() == 4

    def test_more_than_one_word(self):
        self.init()
        stack.append(2)
        word = Word()
        word.append(lambda: stack.append(stack.pop() * 2))
        word.append(lambda: stack.append(stack.pop() * 2))
        word.do()
        assert stack.pop() == 8

    def test_word_calls_word(self):
        self.init()
        stack.append(2)
        double = Word()
        double.append(lambda: stack.append(stack.pop() * 2))
        quad = Word()
        quad.append(double.do)
        quad.append(lambda: double.do())
        quad.do()
        assert stack.pop() == 8

