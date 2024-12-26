import math

from tests.stack import Stack
from tests.word import PrimaryWord, SecondaryWord


class Forth:
    def __init__(self):
        self.stack = Stack()
        self.lexicon = []
        self.define_primaries()
        self.active_words = []

    @property
    def active_word(self):
        return self.active_words[-1]

    def begin(self, word):
        self.active_words.append(word)

    def end(self):
        self.active_words.pop()

    def next_word(self):
        return self.active_word.next_word()

    def define_primaries(self):
        lex = self.lexicon
        self.define_skippers(lex)
        self.define_stack_ops(lex)
        self.define_arithmetic(lex)
        self.define_comparators(lex)
        lex.append(PrimaryWord('SQRT', lambda f: f.stack.push(math.sqrt(f.stack.pop()))))

    @staticmethod
    def define_skippers(lex):
        lex.append(PrimaryWord('*IF', lambda f: f.star_if()))
        lex.append(PrimaryWord('*ELSE', lambda f: f.star_else()))
        lex.append(PrimaryWord('*UNTIL', lambda f: f.star_until()))
        lex.append(PrimaryWord('*#', lambda f: f.stack.push(f.next_word())))

    @staticmethod
    def define_stack_ops(lex):
        lex.append(PrimaryWord('DROP', lambda f: f.stack.pop()))
        lex.append(PrimaryWord('DUP', lambda f: f.stack.dup()))
        lex.append(PrimaryWord('OVER', lambda f: f.stack.over()))
        lex.append(PrimaryWord('ROT', lambda f: f.stack.rot()))
        lex.append(PrimaryWord('SWAP', lambda f: f.stack.swap()))
        lex.append(PrimaryWord('DUMP', lambda f: f.dump_stack()))

    @staticmethod
    def define_arithmetic(lex):
        # swap_pop
        lex.append(PrimaryWord('-', lambda f: f.stack.push(f.stack.swap_pop() - f.stack.pop())))
        lex.append(PrimaryWord('/', lambda f: f.stack.push(f.stack.swap_pop() / f.stack.pop())))
        ## pop
        lex.append(PrimaryWord('+', lambda f: f.stack.push(f.stack.pop() + f.stack.pop())))
        lex.append(PrimaryWord('*', lambda f: f.stack.push(f.stack.pop() * f.stack.pop())))
        lex.append(PrimaryWord('1+', lambda f: f.stack.push(f.stack.pop() + 1)))
        lex.append(PrimaryWord('1-', lambda f: f.stack.push(f.stack.pop() - 1)))

    @staticmethod
    def define_comparators(lex):
        lex.append(PrimaryWord('=', lambda f: f.stack.push(1 if f.stack.pop() == f.stack.pop() else 0)))
        lex.append(PrimaryWord('>', lambda f: f.stack.push(1 if f.stack.pop() > f.stack.pop() else 0)))
        lex.append(PrimaryWord('<', lambda f: f.stack.push(1 if f.stack.pop() < f.stack.pop() else 0)))
        lex.append(PrimaryWord('>=', lambda f: f.stack.push(1 if f.stack.pop() >= f.stack.pop() else 0)))
        lex.append(PrimaryWord('<=', lambda f: f.stack.push(1 if f.stack.pop() <= f.stack.pop() else 0)))

    def compile(self, text):
        words = text.split()
        match words:
            case ':', defining, *rest, ';':
                word_list = self.compile_word_list(rest)
                word = SecondaryWord(defining, word_list)
                self.lexicon.append(word)
                return word
            case _:
                raise SyntaxError(f'Syntax error: "{text}". Missing : or ;?')

    def compile_word_list(self, rest):
        word_list = []
        for word in rest:
            if word == 'IF':
                self.compile_conditional('*IF', word_list)
            elif word == 'THEN':
                self.patch_the_skip(['*IF', '*ELSE'], -1, word_list)
            elif word == 'ELSE':
                self.patch_the_skip(['*IF'], 1, word_list)
                self.compile_conditional('*ELSE', word_list)
            elif word == 'DO':
                self.stack.push(('DO', len(word_list)))
            elif word == 'UNTIL':
                key, jump_loc = self.stack.pop()
                if key != 'DO':
                    raise SyntaxError(f'UNTIL without DO')
                until = self.find_word('*UNTIL')
                word_list.append(until)
                word_list.append(jump_loc - len(word_list) - 1)
            elif (definition := self.find_word(word)) is not None:
                word_list.append(definition)
            elif (num := self.compile_number(word)) is not None:
                definition = self.find_word('*#')
                word_list.append(definition)
                word_list.append(num)
            else:
                raise SyntaxError(f'Syntax error: "{word}" unrecognized')
        return word_list

    def patch_the_skip(self, expected, skip_adjustment, word_list):
        key, patch_loc = self.stack.pop()
        if key not in expected:
            raise SyntaxError(f'malformed IF-ELSE-THEN, found: "{key}"')
        last_loc = len(word_list) + skip_adjustment
        word_list[patch_loc] = last_loc - patch_loc

    def compile_conditional(self, word_to_compile, word_list):
        self.stack.push((word_to_compile, len(word_list) + 1))
        word_list.append(self.find_word(word_to_compile))
        word_list.append(0)

    def compile_number(self, word):
        try:
            num = int(word)
            return num
        except ValueError:
            return None

    def dump_stack(self):
        self.stack.dump()

    def find_word(self, word):
        return next(filter(lambda d: d.name == word, self.lexicon), None)

    def star_if(self):
        jump = self.next_word()
        flag = self.stack.pop()
        if not flag:
            self.active_word.skip(jump)

    def star_else(self):
        self.active_word.skip(self.next_word())

    def star_until(self):
        # if pop is true, skip one else skip in word + 1
        to_check = self.stack.pop()
        skip_back = self.next_word()
        # print(f'*UNTIL has {to_check=} and {skip_back=}')
        if to_check == 0:
            # print('skipping back')
            self.active_word.skip(skip_back)

