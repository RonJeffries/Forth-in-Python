import math
import os
import sys

from source.compile_info import CompileInfo
from source.file_provider import FileProvider
from source.word import Word


class Lexicon:
    def __init__(self):
        self.lexicon = []
        self._latest = None

    def pw(self, name, code, immediate=False):
        self.append(Word(name, [code], immediate=immediate, secondary=False))

    def append(self, word):
        self._latest = word
        self.lexicon.append(word)

    def latest_word(self):
        return self._latest

    def find_word(self, word):
        return next(filter(lambda d: d.name == word, reversed(self.lexicon)), None)

    def words(self, count):
        names = sorted(word.name for word in self.lexicon)
        return ' '.join([f'{name:8s}' + ("\n" if i%count==0 else "") for i, name in enumerate(names)])

    def define_primaries(self, forth):
        self.define_immediate_words(forth)
        self.define_stack_ops()
        self.define_skippers(forth)
        self.define_arithmetic()
        self.define_comparators()
        self.define_logical_operators()
        self.define_case_of_endof_endcase()
        self.define_include()
        self.pw('SQRT', lambda f: f.stack.push(math.sqrt(f.stack.pop())))
        self.pw('.',    lambda f: print(f.stack.pop(), end=' '))
        self.pw('CR',   lambda f: print())
        self.pw('BYE', lambda f: sys.exit())
        self.pw('', lambda f: None)
        self.pw('.CWD', lambda f: print(os.getcwd().strip(), end=' '))
        self.pw('DUMP',   lambda f: f.stack.dump(f.active_word.name, f.active_word.pc))
        self.pw('TRUE', lambda f: f.stack.push(f.true))
        self.pw('FALSE', lambda f: f.stack.push(f.false))
        self.pw('DEPTH', lambda f: f.stack.push(f.stack.size()))
        self.pw('.WORDS', lambda f: print(f.words(f.stack.pop()), end = ' '))
        self.define_secondaries(forth)

    def define_include(self):
        self.pw('INCLUDE', lambda f: f.main_loop(FileProvider(f.next_token())))

    def define_secondaries(self, forth):
        forth.compile_ok(': CONSTANT CREATE , DOES> @ ;')
        forth.compile_ok(': VARIABLE CREATE ;')
        forth.compile_ok(': _DO SWAP >R >R ;')
        forth.compile_ok(': I R@ ;')
        forth.compile_ok(': TUCK SWAP OVER ;')
        forth.compile_ok(': 2OVER 3 PICK 3 PICK ;')
        forth.compile_ok(': 2DROP DROP DROP ;')
        forth.compile_ok(': 2SWAP ROT >R ROT R> ;')
        forth.compile_ok(': /MOD 2DUP MOD ROT ROT / ;')
        forth.compile_ok(': 0= 0 = ;')
        forth.compile_ok(': 0< 0 < ;')
        forth.compile_ok(': 0> 0 > ;')
        forth.compile_ok(': 0<> 0 <> ;')

    def define_immediate_words(self, forth):
        self._define_begin_until()
        self._define_colon_semi()
        self._define_create_does()
        self._define_do_loop()
        self._define_if_else_then()

    def _define_begin_until(self):
        self.pw('BEGIN', lambda f: f.push_compile_info('BEGIN'), immediate=True)
        self.pw('UNTIL', lambda f: f.compile_branching_word('_0BR', 'BEGIN'), immediate=True)

    def _define_colon_semi(self):
        def _colon(forth):
            forth.word_list.clear()
            forth.compile_stack.push(forth.next_token())
            forth.compilation_state = True

        def _semi(forth):
            definition_name = forth.compile_stack.pop()
            word = Word(definition_name, forth.word_list[:])
            forth.lexicon.append(word)
            forth.word_list.clear()
            forth.compilation_state = False

        self.pw(':', _colon, immediate=True)
        self.pw(';', _semi, immediate=True)

    def _define_create_does(self):
        def _create(forth):
            address = forth.heap.next_available()
            literal = forth.find_word('*#')
            name = forth.next_token()
            word = Word(name, [literal, address])
            forth.lexicon.append(word)

        self.pw('DOES>', lambda f: f.active_word.copy_to_latest(f.lexicon))
        self.pw('CREATE', _create)

    def _define_do_loop(self):
        def _do(forth):
            forth.compile_word('_DO')
            forth.push_compile_info('DO')
            # : DO SWAP >R >R ;

        self.pw('DO', _do, immediate=True)
        self.pw('LOOP',
                lambda f: f.compile_branching_word('_LOOP', 'DO'),
                immediate=True)

    def _define_if_else_then(self):
        def _else(forth):
            forth.compile_branch('_BR', 'IF')
            forth.compile_stack.swap_pop().patch('IF')

        self.pw('ELSE', _else, immediate=True)
        self.pw('IF',   lambda f: f.compile_branch('_0BR', 'IF'),   immediate=True)
        self.pw('THEN', lambda f: f.compile_stack.pop().patch('IF'), immediate=True)

    def define_skippers(self, forth):
        self.pw('_LOOP',  lambda f: f.star_loop())
        self.pw('*#',     lambda f: f.stack.push(f.next_word()))

    def define_stack_ops(self):
        self.pw('2DUP',  lambda f: f.stack.two_dup())
        self.pw(',',     lambda f: f.heap.comma(f.stack.pop()))
        self.pw('ALLOT', lambda f: f.heap.allot(f.stack.pop()))
        self.pw('@',     lambda f: f.stack.push(f.heap.at(f.stack.pop())))
        self.pw('!',     lambda f: f.heap.put(f.stack.pop(), f.stack.pop()))
        self.pw('DROP',  lambda f: f.stack.pop())
        self.pw('DUP',   lambda f: f.stack.dup())
        self.pw('OVER',  lambda f: f.stack.over())
        self.pw('ROT',   lambda f: f.stack.rot())
        self.pw('NIP',   lambda f: f.stack.nip())
        self.pw('SWAP',  lambda f: f.stack.swap())
        self.pw('PICK',  lambda f: f.stack.pick())
        self.pw('ROLL',  lambda f: f.stack.roll())
        self.pw('>R',    lambda f: f.return_stack.push(f.stack.pop()))
        self.pw('R>',    lambda f: f.stack.push(f.return_stack.pop()))
        self.pw('R@',    lambda f: f.stack.push(f.return_stack.peek()))

    def define_arithmetic(self):
        self.pw('-',  lambda f: f.stack.push(f.stack.swap_pop() - f.stack.pop()))
        self.pw('%', lambda f: f.stack.push(f.stack.swap_pop() % f.stack.pop()))
        self.pw('MOD', lambda f: f.stack.push(f.stack.swap_pop() % f.stack.pop()))
        self.pw('/',  lambda f: f.stack.push(f.stack.swap_pop() // f.stack.pop()))
        self.pw('+',  lambda f: f.stack.push(f.stack.pop() + f.stack.pop()))
        self.pw('*',  lambda f: f.stack.push(f.stack.pop() * f.stack.pop()))
        self.pw('1+', lambda f: f.stack.push(f.stack.pop() + 1))
        self.pw('1-', lambda f: f.stack.push(f.stack.pop() - 1))

    def define_comparators(self):
        self.pw('=',
                lambda f: f.stack.push(f.true if f.stack.pop() == f.stack.pop() else f.false))
        self.pw('>',
                lambda f: f.stack.push(f.true if f.stack.pop() > f.stack.pop() else f.false))
        self.pw('<',
                lambda f: f.stack.push(f.true if f.stack.pop() < f.stack.pop() else f.false))
        self.pw('>=',
                lambda f: f.stack.push(f.true if f.stack.pop() >= f.stack.pop() else f.false))
        self.pw('<=',
                lambda f: f.stack.push(f.true if f.stack.pop() <= f.stack.pop() else f.false))
        self.pw('<>',
                lambda f: f.stack.push(f.true if f.stack.pop() != f.stack.pop() else f.false))

    def define_logical_operators(self):
        self.pw('OR',
                lambda f: f.stack.push(f.stack.pop() | f.stack.pop()))
        self.pw('AND',
                lambda f: f.stack.push(f.stack.pop() & f.stack.pop()))
        self.pw('INVERT', lambda f: f.stack.push(~f.stack.pop()))

    def define_case_of_endof_endcase(self):
        def _peek_c_s(f):
            f.c_stack_top = f.compile_stack[-1]

        def _endcase(f):
            f.compile_word('DROP')
            f.compile_stack.pop().patch('CASE')

        def _of(f):
            f.compile_word('OVER')
            f.compile_word('=')
            f.compile_branch('_0BR', 'OF')
            f.compile_word('DROP')

        def _endof(f):
            existing_info = f.compile_stack.swap_pop()
            f.compile_branch('_BR', 'CASE')
            f.add_locations_from(existing_info)
            f.compile_stack.swap_pop().patch('OF')

        def _0br(f):
            address = f.next_word()
            if f.stack.pop() == f.false:
                f.active_word.branch(address)

        def _br_tgt(f):
            raise NotImplementedError(f'branch not patched in {f.active_word}')

        self.pw('OF', _of, immediate=True)
        self.pw('ENDOF', _endof, immediate=True)
        self.pw('CASE',
                lambda f: f.compile_stack.push(CompileInfo('CASE', f.word_list)),
                immediate=True)
        self.pw('ENDCASE', _endcase, immediate=True)
        self.pw('_PEEK_C_S', _peek_c_s, immediate=True)
        self.pw('_0BR', _0br)
        self.pw('_BR', lambda f: f.active_word.branch(f.next_word()))
        self.pw('_BR_TGT', _br_tgt)
