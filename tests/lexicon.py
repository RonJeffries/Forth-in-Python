import math

from tests.word import PrimaryWord, SecondaryWord


class Lexicon:
    def __init__(self):
        self.lexicon = []

    def append(self, word):
        self.lexicon.append(word)

    def find_word(self, word):
        return next(filter(lambda d: d.name == word, reversed(self.lexicon)), None)

    def define_primaries(self, forth):
        self.define_immediate_words(forth)
        self.define_stack_ops()
        self.define_skippers(forth)
        self.define_arithmetic()
        self.define_comparators()
        self.append(PrimaryWord('SQRT', lambda f: f.stack.push(math.sqrt(f.stack.pop()))))
        self.append(PrimaryWord('.', lambda f: print(f.stack.pop(), end=' ')))
        self.append(PrimaryWord('CR', lambda f: print()))

    def define_immediate_words(self, forth):
        self._define_begin_until()
        self._define_colon_semi()
        self._define_create_does()
        self._define_do_loop()
        self._define_if_else_then()

    def _define_begin_until(self):
        def _begin(forth):
            forth.compile_stack.push(('BEGIN', len(forth.word_list)))

        def _until(forth):
            key, jump_loc = forth.compile_stack.pop()
            until = forth.find_word('*UNTIL')
            forth.word_list.append(until)
            forth.word_list.append(jump_loc - len(forth.word_list) - 1)

        self.append(PrimaryWord('BEGIN', _begin, immediate=True))
        self.append(PrimaryWord('UNTIL', _until, immediate=True))

    def _define_colon_semi(self):
        def _colon(forth):
            forth.compile_stack.push((':', (forth.next_token())))

        def _semi(forth):
            key, definition_name = forth.compile_stack.pop()
            word = SecondaryWord(definition_name, forth.word_list[:])
            forth.lexicon.append(word)
            forth.word_list.clear()

        self.append(PrimaryWord(':', _colon, immediate=True))
        self.append(PrimaryWord(';', _semi, immediate=True))

    def _define_create_does(self):
        def _create(forth):
            forth.compile_stack.push(('CREATE', forth.next_token()))

        def _does(forth):
            key, definition_name = forth.compile_stack.pop()
            word = SecondaryWord(definition_name, forth.word_list[:])
            forth.lexicon.append(word)
            forth.word_list.clear()

        def _constant(forth):
            name = forth.next_token()
            value = forth.stack.pop()
            literal = forth.find_word('*#')
            word = SecondaryWord(name, [literal, value])
            forth.lexicon.append(word)

        def _variable(forth):
            name = forth.next_token()
            value = len(forth.heap)
            literal = forth.find_word('*#')
            word = SecondaryWord(name, [literal, value])
            forth.lexicon.append(word)

        self.append(PrimaryWord('VARIABLE', _variable))
        self.append(PrimaryWord('CREATE', _create, immediate=True))
        self.append(PrimaryWord('DOES>', _does, immediate=True))
        self.append(PrimaryWord('CONSTANT', _constant))

    def _define_do_loop(self):
        def _do(forth):
            forth.compile_stack.push(('DO', len(forth.word_list)))
            forth.word_list.append(forth.find_word('*DO'))

        def _loop(forth):
            key, jump_loc = forth.compile_stack.pop()
            loop = forth.find_word('*LOOP')
            forth.word_list.append(loop)
            forth.word_list.append(jump_loc - len(forth.word_list))

        self.append(PrimaryWord('DO', _do, immediate=True))
        self.append(PrimaryWord('LOOP', _loop, immediate=True))

    def _define_if_else_then(self):
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

        self.append(PrimaryWord('IF', _if, immediate=True))
        self.append(PrimaryWord('ELSE', _else, immediate=True))
        self.append(PrimaryWord('THEN', _then, immediate=True))

    def define_skippers(self, forth):
        def _2_pc_at(forth):
            forth.stack.push(forth.active_words[-2].pc)

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

        self.append(PrimaryWord('*LOOP', _star_loop))
        self.append(PrimaryWord('*#', lambda f: f.stack.push(_next_word(f))))
        self.append(PrimaryWord('*IF', _zero_branch))
        self.append(PrimaryWord('*ELSE', lambda f: _active_word(f).skip(_next_word(f))))
        self.append(PrimaryWord('*UNTIL', _zero_branch))
        self.append(PrimaryWord('DUMP', _dump_stack))
        self.append(PrimaryWord('2PC@', _2_pc_at))
        forth.compile(': *DO SWAP >R >R ;')
        forth.compile(': I R@ ;')

    def define_stack_ops(self):
        def _2dup(forth):
            top = forth.stack[-1]
            bot = forth.stack[-2]
            forth.stack.push(bot)
            forth.stack.push(top)

        def _at(forth):
            index = forth.stack.pop()
            forth.stack.push(forth.heap[index])

        def _put(forth):
            index = forth.stack.pop()
            value = forth.stack.pop()
            forth.heap[index] = value

        def _allot(forth):
            forth.heap.extend([0]*forth.stack.pop())

        self.append(PrimaryWord('ALLOT', _allot))
        self.append(PrimaryWord('@', _at))
        self.append(PrimaryWord('!', _put))
        self.append(PrimaryWord('2DUP', _2dup))
        self.append(PrimaryWord('DROP', lambda f: f.stack.pop()))
        self.append(PrimaryWord('DUP', lambda f: f.stack.dup()))
        self.append(PrimaryWord('OVER', lambda f: f.stack.over()))
        self.append(PrimaryWord('ROT', lambda f: f.stack.rot()))
        self.append(PrimaryWord('SWAP', lambda f: f.stack.swap()))
        self.append(PrimaryWord('>R', lambda f: f.return_stack.push(f.stack.pop())))
        self.append(PrimaryWord('R>', lambda f: f.stack.push(f.return_stack.pop())))
        self.append(PrimaryWord('R@', lambda f: f.stack.push(f.return_stack.top())))

    def define_arithmetic(self):
        self.define_arithmetic_with_swap_pop()
        self.append(PrimaryWord('+', lambda f: f.stack.push(f.stack.pop() + f.stack.pop())))
        self.append(PrimaryWord('*', lambda f: f.stack.push(f.stack.pop() * f.stack.pop())))
        self.append(PrimaryWord('1+', lambda f: f.stack.push(f.stack.pop() + 1)))
        self.append(PrimaryWord('1-', lambda f: f.stack.push(f.stack.pop() - 1)))

    def define_arithmetic_with_swap_pop(self):
        self.append(PrimaryWord('-', lambda f: f.stack.push(f.stack.swap_pop() - f.stack.pop())))
        self.append(PrimaryWord('/', lambda f: f.stack.push(f.stack.swap_pop() / f.stack.pop())))

    def define_comparators(self):
        self.append(PrimaryWord('=', lambda f: f.stack.push(1 if f.stack.pop() == f.stack.pop() else 0)))
        self.append(PrimaryWord('>', lambda f: f.stack.push(1 if f.stack.pop() > f.stack.pop() else 0)))
        self.append(PrimaryWord('<', lambda f: f.stack.push(1 if f.stack.pop() < f.stack.pop() else 0)))
        self.append(PrimaryWord('>=', lambda f: f.stack.push(1 if f.stack.pop() >= f.stack.pop() else 0)))
        self.append(PrimaryWord('<=', lambda f: f.stack.push(1 if f.stack.pop() <= f.stack.pop() else 0)))

