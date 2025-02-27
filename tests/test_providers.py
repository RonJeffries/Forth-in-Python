from source.file_provider import FileProvider
from source.forth import Forth
from source.keyboard_provider import KeyboardProvider
from source.string_provider import StringProvider


class TestProviders:
    def test_string_provider(self):
        provider = StringProvider('abc def ghi')
        assert provider.has_tokens()
        assert provider.next_token() == 'ABC'
        assert provider.has_tokens()
        assert provider.next_token() == 'DEF'
        assert provider.has_tokens()
        assert provider.next_token() == 'GHI'

    def test_keyboard_provider(self):
        provider = KeyboardProvider()
        provider.set_line('abc def ghi')
        assert provider.has_tokens()
        assert provider.next_token() == 'ABC'
        assert provider.has_tokens()
        assert provider.next_token() == 'DEF'
        assert provider.has_tokens()
        assert provider.next_token() == 'GHI'
        assert provider.has_tokens() # always ready

    def test_open_file(self):
        with open('init.forth', 'r') as file:
            pass

    def test_read_file(self):
        with open('test.forth', 'r') as file:
            lines = file.readlines()
        assert lines[0] == ': c 32 - 5 * 9 / ;\n'
        assert lines[1] == '0 c 32 c -40 c . . .'

    def test_file_provider(self):
        fp = FileProvider('test.forth')
        tokens = []
        while fp.has_tokens():
            tokens.append(fp.next_token())
        assert tokens[0] == ':'
        assert tokens[2] == '32'
        assert tokens[-1] == '.'
        assert tokens[-5] == '-40'

    def test_include(self):
        f = Forth()
        result = f.compile('include test.forth')
        assert result == 'ok'
        word = f.find_word('C')
        print(f'C is {word}')
        f.compile('32 c')
        assert f.stack.pop() == 0
        f.compile('-40 c')
        assert f.stack.pop() == -40
        print(f.stack.stack)
        assert f.stack.is_empty()

