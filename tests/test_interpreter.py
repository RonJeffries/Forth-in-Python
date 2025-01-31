


class IForth:
    def __init__(self):
        self.stack = []

    @staticmethod
    def make_tokens(text):
        return text.split()

    def execute(self, command):
        if command == 'dup':
            self.stack.append(self.stack[-1])


class TestInterpreter:
    def test_exists(self):
        forth = IForth()

    def test_stack(self):
        forth = IForth()
        assert forth.stack == []

    def test_tokens(self):
        forth = IForth()
        tokens = forth.make_tokens('10 dup +')
        assert tokens == ['10', 'dup', '+']

    def test_dup(self):
        forth = IForth()
        forth.stack.append(10)
        forth.execute('dup')
        assert forth.stack == [10, 10]