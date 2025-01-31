


class IForth:
    def __init__(self):
        self.stack = []

    @staticmethod
    def make_tokens(text):
        return text.split()


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