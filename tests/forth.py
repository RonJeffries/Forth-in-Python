import math
import re

from tests.stack import Stack
from tests.word import PrimaryWord, SecondaryWord


class Forth:
    action_tokens = [':', ';','IF', 'THEN', 'ELSE', 'BEGIN', 'UNTIL', 'DO', 'LOOP']

    def __init__(self):
        self.active_words = []
        self.compile_stack = Stack()
        self.lexicon = []
        self.define_primaries()
        self.return_stack = Stack()
        self.stack = Stack()
        self.tokens = None
        self.token_index = 0

    def next_token(self):
        if self.token_index >= len(self.tokens):
            return None
        token = self.tokens[self.token_index]
        self.token_index += 1
        return token

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
        lex.append(PrimaryWord('.', lambda f: print(f.stack.pop(), end=' ')))
        lex.append(PrimaryWord('CR', lambda f: print()))

    @staticmethod
    def define_skippers(lex):
        lex.append(PrimaryWord('*#', lambda f: f.stack.push(f.next_word())))
        lex.append(PrimaryWord('*IF', lambda f: f.star_if()))
        lex.append(PrimaryWord('*ELSE', lambda f: f.star_else()))
        lex.append(PrimaryWord('*UNTIL', lambda f: f.star_until()))
        lex.append(PrimaryWord('*DO', lambda f: f.star_do()))
        lex.append(PrimaryWord('*LOOP', lambda f: f.star_loop()))

    @staticmethod
    def define_stack_ops(lex):
        lex.append(PrimaryWord('DROP', lambda f: f.stack.pop()))
        lex.append(PrimaryWord('DUP', lambda f: f.stack.dup()))
        lex.append(PrimaryWord('OVER', lambda f: f.stack.over()))
        lex.append(PrimaryWord('ROT', lambda f: f.stack.rot()))
        lex.append(PrimaryWord('SWAP', lambda f: f.stack.swap()))
        lex.append(PrimaryWord('DUMP', lambda f: f.dump_stack()))
        lex.append(PrimaryWord('R>', lambda f: f.return_stack.push(f.stack.pop())))
        lex.append(PrimaryWord('>R', lambda f: f.stack.push(f.return_stack.pop())))
        lex.append(PrimaryWord('I', lambda f: f.i_word()))

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
        word_list = []
        while True:
            token = self.next_token()
            if (definition := self.find_word(token)) is not None:
                word_list.append(definition)
            elif token in self.action_tokens:
                self.compile_action_word(token, word_list)
            elif (num := self.compile_number(token)) is not None:
                self.append_number(num, word_list)
            else:
                raise SyntaxError(f'Syntax error: "{token}" unrecognized')
            if self.compile_stack.is_empty():
                break
        return SecondaryWord('nameless', word_list)

    def append_number(self, num, word_list):
        word_list.append(self.find_word('*#'))
        word_list.append(num)

    def compile_action_word(self, word, word_list):
        match word:
            case ':':
                if self.compile_stack.is_not_empty():
                    raise SyntaxError(f'Syntax error: nested word definition')
                if word_list:
                    raise SyntaxError(f'Syntax error: "{word_list}" not empty')
                definition_name = self.next_token()
                self.compile_stack.push((':', definition_name))
            case ';':
                if self.compile_stack.is_empty():
                    raise SyntaxError(f'Syntax error: ; without :')
                key, definition_name = self.compile_stack.pop()
                if key != ':':
                    raise SyntaxError(f'Syntax error: ; without :')
                word = SecondaryWord(definition_name, word_list[:])
                self.lexicon.append(word)
                word_list.clear()
            case 'IF':
                self.compile_conditional('*IF', word_list)
            case 'THEN':
                self.patch_the_skip(['*IF', '*ELSE'], -1, word_list)
            case 'ELSE':
                self.patch_the_skip(['*IF'], 1, word_list)
                self.compile_conditional('*ELSE', word_list)
            case 'BEGIN':
                self.compile_stack.push(('BEGIN', len(word_list)))
            case 'UNTIL':
                key, jump_loc = self.compile_stack.pop()
                if key != 'BEGIN':
                    raise SyntaxError(f'UNTIL without BEGIN')
                until = self.find_word('*UNTIL')
                word_list.append(until)
                word_list.append(jump_loc - len(word_list) - 1)
            case 'DO':
                self.compile_stack.push(('DO', len(word_list)))
                word_list.append(self.find_word('*DO'))
            case 'LOOP':
                key, jump_loc = self.compile_stack.pop()
                if key != 'DO':
                    raise SyntaxError(f'LOOP without DO')
                loop = self.find_word('*LOOP')
                word_list.append(loop)
                word_list.append(jump_loc - len(word_list))

    def patch_the_skip(self, expected, skip_adjustment, word_list):
        key, patch_loc = self.compile_stack.pop()
        if key not in expected:
            raise SyntaxError(f'malformed IF-ELSE-THEN, found: "{key}"')
        last_loc = len(word_list) + skip_adjustment
        word_list[patch_loc] = last_loc - patch_loc

    def compile_conditional(self, word_to_compile, word_list):
        self.compile_stack.push((word_to_compile, len(word_list) + 1))
        word_list.append(self.find_word(word_to_compile))
        word_list.append(0)

    def compile_number(self, word):
        try:
            num = int(word)
            return num
        except ValueError:
            return None

    def dump_stack(self):
        self.stack.dump(self.active_word.name, self.active_word.pc)

    def find_word(self, word):
        return next(filter(lambda d: d.name == word, self.lexicon), None)

    def i_word(self):
        index, limit = self.return_stack[-1]
        self.stack.push(index)

    def star_do(self):
        start = self.stack.pop()
        limit = self.stack.pop()
        self.return_stack.push((start, limit))

    def star_loop(self):
        jump = self.next_word()
        index, limit = self.return_stack.pop()
        index += 1
        if index < limit:
            self.return_stack.push((index, limit))
            self.active_word.skip(jump)

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
        if to_check == 0:
            self.active_word.skip(skip_back)

