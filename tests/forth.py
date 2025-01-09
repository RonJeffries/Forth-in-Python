import math
import re

from tests.lexicon import Lexicon
from tests.stack import Stack
from tests.word import PrimaryWord, SecondaryWord


class Forth:
    def __init__(self):
        self.active_words = []
        self.compile_stack = Stack()
        self.heap = [0]
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
        if self.token_index >= len(self.tokens):
            return None
        token = self.tokens[self.token_index]
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
            self.compile_a_word().do(self)

    def compile_a_word(self):
        self.word_list = []
        while True:
            token = self.next_token()
            if (definition := self.find_word(token)) is not None:
                if definition.immediate:
                    definition.do(self)
                else:
                    self.word_list.append(definition)
            elif (num := self.compile_number(token)) is not None:
                self.append_number(num, self.word_list)
            else:
                raise SyntaxError(f'Syntax error: "{token}" unrecognized')
            if self.compile_stack.is_empty():
                break
        return SecondaryWord('nameless', self.word_list)

    def append_number(self, num, word_list):
        word_list.append(self.find_word('*#'))
        word_list.append(num)

    def compile_number(self, word):
        try:
            return int(word)
        except ValueError:
            return None

    def find_word(self, word):
        return self.lexicon.find_word(word)
