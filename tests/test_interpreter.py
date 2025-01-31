


class IForth:
    def __init__(self):
        self.stack = []


class TestInterpreter:
    def test_exists(self):
        forth = IForth()

    def test_stack(self):
        forth = IForth()
        assert forth.stack == []