class Stack:
    def __init__(self):
        self.stack = []

    def dump(self):
        print(self.stack)

    def dup(self):
        self.push(self.stack[-1])

    def extend(self, items):
        self.stack.extend(items)

    def over(self):
        self.push(self.stack[-2])

    def pop(self):
        return self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    def rot(self):
        stack = self.stack
        top, middle, bottom  = stack.pop(), stack.pop(), stack.pop()
        self.extend([middle, top, bottom])

    def swap(self):
        stack = self.stack
        top, under = stack.pop(), stack.pop()
        self.extend([top, under])

    def swap_pop(self):
        # (_ under top -> _ top ) -> under
        self.swap()
        return self.pop()

    def __eq__(self, other):
        return self.stack == other
