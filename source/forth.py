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
        if self.active_words:
            return self.active_words[-1]
        else:
            return Word('no active word', [])

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
            self.process_line(text)
        except Exception as e:
            msg = str(e)
            if msg  == 'Unexpected end of input':
                return '...'
            else:
                self.abend()
                return f'{e} ?'
        return 'ok'

    def process_line(self, text):
        new_text = re.sub(r'\(.*?\)', ' ', text)
        self.tokens = new_text.split()
        self.token_index = 0
        while self.token_index < len(self.tokens):
            self.process_token(self.next_token())
        if self.compilation_state:
            raise ValueError('Unexpected end of input')

    def process_token(self, token):
        definition = self.get_definition(token)
        if not self.compilation_state or definition.immediate:
            definition(self)
        else:
            self.word_list.append(definition)

    def get_definition(self, token):
        if definition := self.find_word(token):
            return definition
        elif (num := self.get_literal(token)) is not None:  # might be zero
            return num
        else:
            raise SyntaxError(f'Syntax error: "{token}" unrecognized')

    def get_literal(self, token):
        try:
            return Word('', [self.find_word('*#'), int(token)])
        except ValueError:
            return None

    def find_word(self, word):
        return self.lexicon.find_word(word)
