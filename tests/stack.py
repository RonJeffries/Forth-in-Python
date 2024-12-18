class Stack:
    def __init__(self):
        self.stack = []

    def dup(self):
        self.push(self.stack[-1])

    def extend(self, words):
        self.stack.extend(words)

    def over(self):
        self.push(self.stack[-2])

    def pop(self):
        return self.stack.pop()

    def push(self, word):
        self.stack.append(word)

    def rot(self):
        stack = self.stack
        top, middle, bottom  = stack.pop(), stack.pop(), stack.pop()
        stack.extend([middle, top, bottom])

    def swap(self):
        stack = self.stack
        top, under = stack.pop(), stack.pop()
        self.extend([top, under])

    def swap_pop(self):
        # (_ under top -> _ top ) -> under
        self.swap()
        return self.stack.pop()

    def __eq__(self, other):
        return self.stack == other
