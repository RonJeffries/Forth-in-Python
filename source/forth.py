import re

from source.heap import Heap
from source.lexicon import Lexicon
from source.stack import Stack
from source.word import Word


class Forth:
    def __init__(self):
        self.active_words = []
        self.compile_stack = Stack()
        self.heap = Heap()
        self.lexicon = Lexicon()
        self.lexicon.define_primaries(self)
        self.return_stack = Stack()
        self.stack = Stack()
        self.tokens = None
        self.token_index = 0
        self.word_list = None

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
        new_text = re.sub(r'\(.*?\)', ' ', text)
        self.tokens = new_text.split()
        self.token_index = 0
        while self.token_index < len(self.tokens):
            word = self.compile_a_word()
            word(self)

    def compile_a_word(self):
        self.word_list = []
        while True:
            token = self.next_token()
            if token is None:
                raise ValueError('Unexpected end of input')
            if (definition := self.find_word(token)) is not None:
                if definition.immediate:
                    definition(self)
                else:
                    self.word_list.append(definition)
            elif (num := self.parse_number(token)) is not None:
                self.compile_literal(num, self.word_list)
            else:
                raise SyntaxError(f'Syntax error: "{token}" unrecognized')
            if self.compile_stack.is_empty():
                break
        return Word('nameless', self.word_list)

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
