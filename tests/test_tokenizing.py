
def split_off_token(line):
    trimmed = line.lstrip()
    index = trimmed.find(' ')
    if index == -1:
        return trimmed, ''
    else:
        return trimmed[:index], trimmed[index:]


class TestTokenizing:
    def test_get_token(self):
        line = '  abc '
        index = 0
        skipping = True
        token = ''
        while index < len(line):
            char = line[index]
            if char == ' ' and skipping:
                index += 1
            else:
                skipping = False
                if char != ' ':
                    token += char
                    index += 1
                else:
                    break
        assert token == 'abc'
        assert index == 5


    def test_split_off_token(self):
        line = 'abc d ef g hij'
        token, line = split_off_token(line)
        assert token == 'abc'
        token, line = split_off_token(line)
        assert token == 'd'
        token, line = split_off_token(line)
        assert token == 'ef'
        token, line = split_off_token(line)
        assert token == 'g'
        token, line = split_off_token(line)
        assert token == 'hij'


