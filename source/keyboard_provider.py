from source.string_provider import StringProvider


class KeyboardProvider:
    def __init__(self):
        self.provider = StringProvider('')

    def has_tokens(self):
        return True

    def next_token(self):
        if not self.provider.has_tokens():
            self.set_line(input('Forth>'))
        return self.provider.next_token()

    def set_line(self, line):
        self.provider = StringProvider(line)
