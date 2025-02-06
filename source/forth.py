import re

from source.heap import Heap
from source.lexicon import Lexicon
from source.stack import Stack
from source.word import Word


class Forth:
    def __init__(self):
        self.active_words = []
        self.compile_stack = Stack()
        self.compilation_state = False
        self.heap = Heap()
        self.lexicon = Lexicon()
        self.return_stack = Stack()
        self.stack = Stack()
        self.tokens = None
        self.token_index = 0
        self.word_list = []
        self.lexicon.define_primaries(self)

    def abend(self):
        self.stack.clear()
        self.compile_stack.clear()
        self.return_stack.clear()
        self.active_words = []

    @property
    def active_word(self):
        return self.active_words[-1]

    def next_token(self):
        try:
            token = self.tokens[self.token_index]
        except IndexError:
            return None
        self.token_index += 1
        return token.upper()

    def begin(self, word):
        self.active_words.append(word)

    def end(self):
        self.active_words.pop()

    def compile(self, text):
        try:
            self.unsafe_compile(text)
        except Exception as e:
            msg = str(e)
            if msg  == 'Unexpected end of input':
                return '...'
            else:
                self.abend()
                return f'{e} ?'
        return 'ok'

    def unsafe_compile(self, text):
        new_text = re.sub(r'\(.*?\)', ' ', text)
        self.tokens = new_text.split()
        self.token_index = 0
        while self.token_index < len(self.tokens):
            word = self.compile_a_word()
            word(self)

    def compile_a_word(self):
        while True:
            token = self.next_token()
            if token is None:
                raise ValueError('Unexpected end of input')
            found_word = self.find_word_or_literal(token)
            if not self.compilation_state:
                return found_word
            if found_word.immediate:
                found_word(self)
            else:
                self.word_list.append(found_word)
            if not self.compilation_state:
                return Word('no-op', [])

    def find_word_or_literal(self, token):
        found_word = self.find_word(token)
        if found_word:
            return found_word
        num = self.parse_number(token)
        if num is not None:  # might be zero
            literal = self.find_word('*#')
            return Word('', [literal, num])
        else:
            raise SyntaxError(f'Syntax error: "{token}" unrecognized')

    def compile_literal(self, num, word_list):
        word_list.append(self.find_word('*#'))
        word_list.append(num)

    def parse_number(self, word):
        try:
            return int(word)
        except ValueError:
            return None

    def find_word(self, word):
        return self.lexicon.find_word(word)
