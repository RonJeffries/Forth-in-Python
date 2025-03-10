
class Stack:
    def __init__(self, limit=100):
        self.stack = []
        self.limit = limit

    def __eq__(self, other):
        return other == self.stack

    def __getitem__(self, item):
        return self.stack[item]

    def _check_limit(self):
        if len(self.stack) > self.limit:
            raise ValueError("Stack is full")

    def is_not_empty(self):
        return len(self.stack) > 0

    def is_empty(self):
        return len(self.stack) == 0

    def clear(self):
        self.stack.clear()

    def flush(self):
        copy = self.stack[:]
        self.stack.clear()
        return copy

    def dump(self, name, pc):
        print(f'{name}[{pc}]: {self.stack}')

    def dup(self):
        self.push(self.stack[-1])

    def extend(self, items):
        self.stack.extend(items)
        self._check_limit()

    def nip(self):
        top, nip = self.pop(), self.pop()
        self.push(top)

    def over(self):
        self.push(self.stack[-2])

    def peek(self):
        return self.stack[-1]

    def peek_under(self):
        return self.stack[-2]

    def pick(self):
        index = -1 - self.pop()
        self.push(self.stack[index])

    def roll(self):
        index = -1 - self.pop()
        self.push(self.stack.pop(index))

    # pick ( xu...x1 x0 u -- xu...x1 x0 xu )
    # roll ( xu xu-1 ... x0 u -- xu-1 ... x0 xu )

    def pop(self):
        return self.stack.pop()

    def push(self, item):
        self.stack.append(item)
        self._check_limit()

    def rot(self):
        stack = self.stack
        stack[-1], stack[-2], stack[-3]  = stack[-3], stack[-1], stack[-2]
        # top, middle, bottom  =            bottom     top        middle

    def size(self):
        return len(self.stack)

    def swap(self):
        stack = self.stack
        stack[-1], stack[-2] = stack[-2], stack[-1]

    def swap_pop(self):
        # (_ under top -> _ top ) -> under
        return self.stack.pop(-2)

    def two_dup(self):
        self.extend(self.stack[-2:])