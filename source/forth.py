import re

from source.compile_info import CompileInfo
from source.heap import Heap
from source.lexicon import Lexicon
from source.stack import Stack
from source.word import Word


class Forth:
    true = -1
    false = 0

    def __init__(self):
        self.active_words = []
        self.compile_stack = Stack()
        self.compilation_state = False
        self.c_stack_top = None
        self.heap = Heap()
        self.return_stack = Stack()
        self.stack = Stack()
        self.tokens = None
        self.token_index = 0
        self.word_list = []
        self.lexicon = Lexicon()
        self.lexicon.define_primaries(self)

    def abend(self):
        self.stack.clear()
        self.compile_stack.clear()
        self.compilation_state = False
        self.return_stack.clear()
        self.active_words = []

    @property
    def active_word(self):
        if self.active_words:
            return self.active_words[-1]
        else:
            return Word('no active word', [])

    def append_word(self, word):
        self.word_list.append(word)

    def compile_branch(self, branch_name, info_name):
        self.compile_word(branch_name)
        self.push_compile_info(info_name)
        self.compile_word('BR_TARGET')

    def compile_branching_word(self, branch_name, info_name):
        self.compile_word(branch_name)
        info = self.compile_stack.pop()
        assert info.name == info_name, f'{info.name} != {info_name}'
        self.append_word(info.locations[0])

    def push_compile_info(self, info_name):
        info = CompileInfo(info_name, self.word_list)
        self.compile_stack.push(info)
        self.update_branch()

    def update_branch(self):
        top = self.compile_stack.top()
        top.add_current_location(top.name)

    def star_loop(self):
            new_index = self.return_stack.pop() + 1
            limit = self.return_stack.pop()
            beginning_of_do_loop = self.next_word()
            if new_index < limit:
                self.return_stack.push(limit)
                self.return_stack.push(new_index)
                self.active_word.branch(beginning_of_do_loop)

    def add_locations_from(self, info):
        self.compile_stack.top().add_locations_from(info)

    def compile_word(self, word_name):
        self.append_word(self.find_word(word_name))

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

    def next_word(self):
        return self.active_word.next_word()

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
            return Word(f'*# {int(token)}', [self.find_word('*#'), int(token)])
        except ValueError:
            return None

    def find_word(self, word):
        return self.lexicon.find_word(word)
