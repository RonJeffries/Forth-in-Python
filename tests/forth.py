import math
import re

from tests.lexicon import Lexicon
from tests.stack import Stack
from tests.word import PrimaryWord, SecondaryWord


class Forth:
    def __init__(self):
        self.active_words = []
        self.compile_stack = Stack()
        self.lexicon = Lexicon()
        self.define_primaries(self.lexicon)
        self.return_stack = Stack()
        self.stack = Stack()
        self.tokens = None
        self.token_index = 0
        self.word_list = None

    def next_token(self):
        if self.token_index >= len(self.tokens):
            return None
        token = self.tokens[self.token_index]
        self.token_index += 1
        return token

    def begin(self, word):
        self.active_words.append(word)

    def end(self):
        self.active_words.pop()

    def define_primaries(self, lex):
        self.define_stack_ops(lex)
        self.define_immediate_words(lex)
        self.define_skippers(lex)
        self.define_arithmetic(lex)
        self.define_comparators(lex)
        lex.append(PrimaryWord('SQRT', lambda f: f.stack.push(math.sqrt(f.stack.pop()))))
        lex.append(PrimaryWord('.', lambda f: print(f.stack.pop(), end=' ')))
        lex.append(PrimaryWord('CR', lambda f: print()))

    def define_immediate_words(self, lex):
        self._define_begin_until(lex)
        self._define_colon_semi(lex)
        self._define_do_loop(lex)
        self._define_if_else_then(lex)

    @staticmethod
    def _define_begin_until(lex):
        def _begin(forth):
            forth.compile_stack.push(('BEGIN', len(forth.word_list)))

        def _until(forth):
            key, jump_loc = forth.compile_stack.pop()
            until = forth.find_word('*UNTIL')
            forth.word_list.append(until)
            forth.word_list.append(jump_loc - len(forth.word_list) - 1)

        lex.append(PrimaryWord('BEGIN', _begin, immediate=True))
        lex.append(PrimaryWord('UNTIL', _until, immediate=True))

    @staticmethod
    def _define_colon_semi(lex):
        def _colon(forth):
            forth.compile_stack.push((':', (forth.next_token())))

        def _semi(forth):
            key, definition_name = forth.compile_stack.pop()
            word = SecondaryWord(definition_name, forth.word_list[:])
            forth.lexicon.append(word)
            forth.word_list.clear()

        lex.append(PrimaryWord(':', _colon, immediate=True))
        lex.append(PrimaryWord(';', _semi, immediate=True))

    @staticmethod
    def _define_do_loop(lex):
        def _do(forth):
            forth.compile_stack.push(('DO', len(forth.word_list)))
            forth.word_list.append(forth.find_word('*DO'))

        def _loop(forth):
            key, jump_loc = forth.compile_stack.pop()
            loop = forth.find_word('*LOOP')
            forth.word_list.append(loop)
            forth.word_list.append(jump_loc - len(forth.word_list))

        lex.append(PrimaryWord('DO', _do, immediate=True))
        lex.append(PrimaryWord('LOOP', _loop, immediate=True))

    @staticmethod
    def _define_if_else_then(lex):
        def _compile_conditional(forth, word_to_compile, word_list):
            forth.compile_stack.push((word_to_compile, len(word_list) + 1))
            word_list.append(forth.find_word(word_to_compile))
            word_list.append(0)

        def _patch_the_skip(forth, expected, skip_adjustment, word_list):
            key, patch_loc = forth.compile_stack.pop()
            last_loc = len(word_list) + skip_adjustment
            word_list[patch_loc] = last_loc - patch_loc

        def _if(forth):
            _compile_conditional(forth,'*IF', forth.word_list)

        def _else(forth):
            _patch_the_skip(forth, ['*IF'], 1, forth.word_list)
            _compile_conditional(forth, '*ELSE', forth.word_list)

        def _then(forth):
            _patch_the_skip(forth, ['*IF', '*ELSE'], -1, forth.word_list)

        lex.append(PrimaryWord('IF', _if, immediate=True))
        lex.append(PrimaryWord('ELSE', _else, immediate=True))
        lex.append(PrimaryWord('THEN', _then, immediate=True))

    def define_skippers(self,lex):
        def _active_word(forth):
            return forth.active_words[-1]

        def _next_word(forth):
            return _active_word(forth).next_word()

        def _star_loop(forth):
            beginning_of_do_loop = _next_word(forth)
            index = forth.return_stack.pop()
            limit = forth.return_stack.pop()
            index += 1
            if index < limit:
                forth.return_stack.push(limit)
                forth.return_stack.push(index)
                _active_word(forth).skip(beginning_of_do_loop)

        def _zero_branch(forth):
            branch_distance = _next_word(forth)
            if forth.stack.pop() == 0:
                _active_word(forth).skip(branch_distance)

        def _dump_stack(forth):
            forth.stack.dump(_active_word(forth).name, _active_word(forth).pc)

        lex.append(PrimaryWord('*LOOP', _star_loop))
        lex.append(PrimaryWord('*#', lambda f: f.stack.push(_next_word(f))))
        lex.append(PrimaryWord('*IF', _zero_branch))
        lex.append(PrimaryWord('*ELSE', lambda f: _active_word(f).skip(_next_word(f))))
        lex.append(PrimaryWord('*UNTIL', _zero_branch))
        lex.append(PrimaryWord('DUMP', _dump_stack))
        self.compile(': *DO SWAP >R >R ;')
        self.compile(': I R@ ;')

    @staticmethod
    def define_stack_ops(lex):
        def _2dup(forth):
            top = forth.stack[-1]
            bot = forth.stack[-2]
            forth.stack.push(bot)
            forth.stack.push(top)

        lex.append(PrimaryWord('2DUP', _2dup))
        lex.append(PrimaryWord('DROP', lambda f: f.stack.pop()))
        lex.append(PrimaryWord('DUP', lambda f: f.stack.dup()))
        lex.append(PrimaryWord('OVER', lambda f: f.stack.over()))
        lex.append(PrimaryWord('ROT', lambda f: f.stack.rot()))
        lex.append(PrimaryWord('SWAP', lambda f: f.stack.swap()))
        lex.append(PrimaryWord('>R', lambda f: f.return_stack.push(f.stack.pop())))
        lex.append(PrimaryWord('R>', lambda f: f.stack.push(f.return_stack.pop())))
        lex.append(PrimaryWord('R@', lambda f: f.stack.push(f.return_stack.top())))

    def define_arithmetic(self, lex):
        self.define_arithmetic_with_swap_pop(lex)
        lex.append(PrimaryWord('+', lambda f: f.stack.push(f.stack.pop() + f.stack.pop())))
        lex.append(PrimaryWord('*', lambda f: f.stack.push(f.stack.pop() * f.stack.pop())))
        lex.append(PrimaryWord('1+', lambda f: f.stack.push(f.stack.pop() + 1)))
        lex.append(PrimaryWord('1-', lambda f: f.stack.push(f.stack.pop() - 1)))

    @staticmethod
    def define_arithmetic_with_swap_pop(lex):
        lex.append(PrimaryWord('-', lambda f: f.stack.push(f.stack.swap_pop() - f.stack.pop())))
        lex.append(PrimaryWord('/', lambda f: f.stack.push(f.stack.swap_pop() / f.stack.pop())))

    @staticmethod
    def define_comparators(lex):
        lex.append(PrimaryWord('=', lambda f: f.stack.push(1 if f.stack.pop() == f.stack.pop() else 0)))
        lex.append(PrimaryWord('>', lambda f: f.stack.push(1 if f.stack.pop() > f.stack.pop() else 0)))
        lex.append(PrimaryWord('<', lambda f: f.stack.push(1 if f.stack.pop() < f.stack.pop() else 0)))
        lex.append(PrimaryWord('>=', lambda f: f.stack.push(1 if f.stack.pop() >= f.stack.pop() else 0)))
        lex.append(PrimaryWord('<=', lambda f: f.stack.push(1 if f.stack.pop() <= f.stack.pop() else 0)))

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
            num = int(word)
            return num
        except ValueError:
            return None

    def find_word(self, word):
        return self.lexicon.find_word(word)
