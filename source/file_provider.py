from source.string_provider import StringProvider


class FileProvider:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
        self.line_number = 0
        self.reader = StringProvider()

    def has_tokens(self):
        return self.reader.has_tokens() or self._has_lines_left()

    def _has_lines_left(self):
        return self.line_number < len(self.lines)

    def next_token(self):
        if not self.reader.has_tokens() and self._has_lines_left():
            self.reader = StringProvider(self.lines[self.line_number])
            self.line_number += 1
        return self.reader.next_token()