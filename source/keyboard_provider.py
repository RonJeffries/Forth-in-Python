from source.string_provider import StringProvider


class KeyboardProvider:
    def __init__(self, forth=None):
        self.provider = StringProvider('')
        self.forth = forth

    def has_tokens(self):
        return True

    def next_token(self):
        if not self.provider.has_tokens():
            self.set_line(input('Forth>'))
        return self.provider.next_token()

    def set_line(self, line):
        self.provider = StringProvider(line)
