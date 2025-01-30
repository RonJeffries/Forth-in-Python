import math

from source.word import SecondaryWord


class Lexicon:
    def __init__(self):
        self.lexicon = []
        self._latest = None

    def pw(self, name, code, immediate=False):
        self.append(SecondaryWord(name, [code], immediate=immediate, secondary=False))

    def append(self, word):
        self._latest = word
        self.lexicon.append(word)

    def latest_word(self):
        return self._latest

    def find_word(self, word):
        return next(filter(lambda d: d.name == word, reversed(self.lexicon)), None)

    def define_primaries(self, forth):
        self.define_immediate_words(forth)
        self.define_stack_ops()
        self.define_skippers(forth)
        self.define_arithmetic()
        self.define_comparators()
        self.pw('SQRT', lambda f: f.stack.push(math.sqrt(f.stack.pop())))
        self.pw('.',    lambda f: print(f.stack.pop(), end=' '))
        self.pw('CR',   lambda f: print())
        self.define_secondaries(forth)

    def define_secondaries(self, forth):
        forth.compile(': CONSTANT CREATE , DOES> @ ;')
        forth.compile(': VARIABLE CREATE ;')
        forth.compile(': *DO SWAP >R >R ;')
        forth.compile(': I R@ ;')

    def define_immediate_words(self, forth):
        self._define_begin_until()
        self._define_colon_semi()
        self._define_create_does()
        self._define_do_loop()
        self._define_if_else_then()

    def _define_begin_until(self):
        def _until(forth):
            until = forth.find_word('*UNTIL')
            forth.word_list.append(until)
            jump_loc = forth.compile_stack.pop()
            forth.word_list.append(jump_loc - len(forth.word_list) - 1)

        self.pw('BEGIN', lambda f: f.compile_stack.push(len(f.word_list)), immediate=True)
        self.pw('UNTIL', _until, immediate=True)

    def _define_colon_semi(self):
        def _semi(forth):
            definition_name = forth.compile_stack.pop()
            word = SecondaryWord(definition_name, forth.word_list[:])
            forth.lexicon.append(word)
            forth.word_list.clear()

        self.pw(':', lambda f: f.compile_stack.push(f.next_token()), immediate=True)
        self.pw(';', _semi, immediate=True)

    def _define_create_does(self):
        def _create(forth):
            address = forth.heap.next_available()
            literal = forth.find_word('*#')
            name = forth.next_token()
            word = SecondaryWord(name, [literal, address])
            forth.lexicon.append(word)

        self.pw('DOES>', lambda f: f.active_word.copy_to_latest(f.lexicon))
        self.pw('CREATE', _create)

    def _define_do_loop(self):
        def _do(forth):
            forth.compile_stack.push(len(forth.word_list))
            forth.word_list.append(forth.find_word('*DO'))

        def _loop(forth):
            jump_loc = forth.compile_stack.pop()
            loop = forth.find_word('*LOOP')
            forth.word_list.append(loop)
            forth.word_list.append(jump_loc - len(forth.word_list))

        self.pw('DO', _do, immediate=True)
        self.pw('LOOP', _loop, immediate=True)

    def _define_if_else_then(self):
        def _compile_conditional(forth, word_to_compile, word_list):
            forth.compile_stack.push(len(word_list) + 1)
            word_list.append(forth.find_word(word_to_compile))
            word_list.append(0)

        def _patch_the_skip(forth, skip_adjustment, word_list):
            patch_loc = forth.compile_stack.pop()
            last_loc = len(word_list) + skip_adjustment
            word_list[patch_loc] = last_loc - patch_loc

        def _if(forth):
            _compile_conditional(forth,'*IF', forth.word_list)

        def _else(forth):
            _patch_the_skip(forth, 1, forth.word_list)
            _compile_conditional(forth, '*ELSE', forth.word_list)

        def _then(forth):
            _patch_the_skip(forth, -1, forth.word_list)

        self.pw('IF',   _if,   immediate=True)
        self.pw('ELSE', _else, immediate=True)
        self.pw('THEN', _then, immediate=True)

    def define_skippers(self, forth):
        def _next_word(forth):
            return forth.active_word.next_word()

        def _star_loop(forth):
            beginning_of_do_loop = _next_word(forth)
            index = forth.return_stack.pop()
            limit = forth.return_stack.pop()
            index += 1
            if index < limit:
                forth.return_stack.push(limit)
                forth.return_stack.push(index)
                forth.active_word.skip(beginning_of_do_loop)

        def _zero_branch(forth):
            branch_distance = _next_word(forth)
            if forth.stack.pop() == 0:
                forth.active_word.skip(branch_distance)

        self.pw('*LOOP',  _star_loop)
        self.pw('*IF',    _zero_branch)
        self.pw('*UNTIL', _zero_branch)
        self.pw('*#',     lambda f: f.stack.push(_next_word(f)))
        self.pw('*ELSE',  lambda f: f.active_word.skip(_next_word(f)))
        self.pw('DUMP',   lambda f: f.stack.dump(f.active_word.name, f.active_word.pc))

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
        self.pw('SWAP',  lambda f: f.stack.swap())
        self.pw('>R',    lambda f: f.return_stack.push(f.stack.pop()))
        self.pw('R>',    lambda f: f.stack.push(f.return_stack.pop()))
        self.pw('R@',    lambda f: f.stack.push(f.return_stack.top()))
        dup_lambda = lambda f: f.stack.dup()
        dup_word = SecondaryWord('DUP', [dup_lambda])
        self.append(dup_word)

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
        self.pw('=',  lambda f: f.stack.push(1 if f.stack.pop() == f.stack.pop() else 0))
        self.pw('>',  lambda f: f.stack.push(1 if f.stack.pop() > f.stack.pop() else 0))
        self.pw('<',  lambda f: f.stack.push(1 if f.stack.pop() < f.stack.pop() else 0))
        self.pw('>=', lambda f: f.stack.push(1 if f.stack.pop() >= f.stack.pop() else 0))
        self.pw('<=', lambda f: f.stack.push(1 if f.stack.pop() <= f.stack.pop() else 0))

