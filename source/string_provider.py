class StringProvider:
    def __init__(self, text=''):
        self.input_line = text

    def has_tokens(self):
        return self.input_line

    def next_token(self):
        trimmed = self.input_line.strip()
        index = trimmed.find(' ')
        if index == -1:
            token, self.input_line = trimmed.upper(), ''
        else:
            token, self.input_line = trimmed[:index].upper(), trimmed[index+1:].strip()
        return token
