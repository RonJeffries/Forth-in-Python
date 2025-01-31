


class IForth:
    def __init__(self):
        self.stack = []
        self.if_active = False
        self.if_words = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    @staticmethod
    def make_tokens(text):
        return text.split()

    def execute_line(self, line):
        for token in self.make_tokens(line):
            self.execute(token)

    def execute(self, command):
        if self.if_active:
            self.handle_if(command)
            return

        if command == 'dup':
            self.stack.append(self.stack[-1])
        elif command == "+":
            self.push(self.pop() + self.pop())
        elif command == 'if':
            self.if_active = True
            self.if_words = []
        elif self.was_number(command):
            pass

    def handle_if(self, command):
        if command == 'then':
            self.if_active = False
            result = self.pop()
            if result != 0:
                line = ' '.join(self.if_words)
                self.if_words = []
                self.execute_line(line)
                return
        else:
            self.if_words.append(command)
            return

    def was_number(self, command):
        try:
            number = int(command)
            self.push(number)
            return True
        except ValueError:
            return False


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

    def test_plus(self):
        forth = IForth()
        forth.stack.append(10)
        forth.stack.append(32)
        forth.execute('+')
        assert forth.stack == [42]

    def test_dup_plus(self):
        forth = IForth()
        forth.stack.append(21)
        forth.execute_line('dup +')
        assert forth.stack == [42]

    def test_numbers(self):
        forth = IForth()
        forth.execute_line('11 31 +')
        assert forth.stack == [42]

    def test_if_then_true(self):
        forth = IForth()
        forth.execute_line('21 1 if dup + then')
        assert forth.stack == [42]

    def test_if_then_false(self):
        forth = IForth()
        forth.execute_line('21 0 if dup + then')
        assert forth.stack == [21]