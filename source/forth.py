import re

from source.compile_info import CompileInfo
from source.heap import Heap
from source.lexicon import Lexicon
from source.stack import Stack
from source.string_provider import StringProvider
from source.word import Word


class Forth:
    true = -1
    false = 0

    def __init__(self):
        self.provider = None
        self.result = ''
        self.abend()
        self.lexicon = Lexicon()
        self.lexicon.define_primaries(self)

    # noinspection PyAttributeOutsideInit
    def abend(self):
        self.active_words = Stack()
        self.compile_stack = Stack()
        self.compilation_state = False
        self.c_stack_top = None
        self.heap = Heap()
        self.provider = StringProvider('')
        self.return_stack = Stack()
        self.stack = Stack()
        self.word_list = []
        self.stack.clear()

    @property
    def active_word(self):
        if self.active_words:
            return self.active_words.peek()
        else:
            return Word('no active word', [])

    def append_word(self, word):
        self.word_list.append(word)

    def compile_branch(self, branch_name, info_name):
        self.compile_word(branch_name)
        self.push_compile_info(info_name)
        self.compile_word('BR_TARGET')

    def push_compile_info(self, info_name):
        info = CompileInfo(info_name, self.word_list)
        self.compile_stack.push(info)
        self.update_branch()

    def update_branch(self):
        top = self.compile_stack.peek()
        top.add_current_location(top.name)

    def compile_branching_word(self, branch_name, info_name):
        self.compile_word(branch_name)
        info = self.compile_stack.pop()
        assert info.name == info_name, f'{info.name} != {info_name}'
        self.append_word(info.locations[0])

    def star_loop(self):
        new_index = self.return_stack.pop() + 1
        limit = self.return_stack.pop()
        beginning_of_do_loop = self.next_word()
        if new_index < limit:
            self.return_stack.push(limit)
            self.return_stack.push(new_index)
            self.active_word.branch(beginning_of_do_loop)

    def add_locations_from(self, info):
        self.compile_stack.peek().add_locations_from(info)

    def compile_word(self, word_name):
        self.append_word(self.find_word(word_name))

    def begin(self, word):
        self.active_words.push(word)

    def end(self):
        self.active_words.pop()

    def compile(self, text):
        clean_line = re.sub(r'\(.*?\)', ' ', text)
        provider = StringProvider(clean_line)
        return self.main_loop(provider)

    def main_loop(self, provider):
        self.provider = provider
        while self.provider.has_tokens():
            try:
                self.process_token(self.provider.next_token())
            except Exception as e:
                self.result = f'{e} ?'
                self.abend()
            else:
                self.result = 'ok'
        if self.compilation_state:
            return 'Unexpected end of input ?'
        return self.result

    def process_token(self, token):
        definition = self.get_definition(token)
        if not self.compilation_state or definition.immediate:
            definition(self)
        else:
            self.append_word(definition)

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

    def next_token(self):
        return self.provider.next_token()

    def next_word(self):
        return self.active_word.next_word()

    def find_word(self, word):
        return self.lexicon.find_word(word)
