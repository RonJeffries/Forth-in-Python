

class TestPython:
    def test_hook(self):
        assert True

    def test_rot(self):
        s = [0, 1, 2, 3, 4, 5, 6]
        s1 = s[0:-3]
        assert s1 == [0, 1, 2, 3, ]
        s2 = s[-3:-2]
        assert s2 == [4]
        s3 = s[-2:]
        assert s3 == [5, 6]
        new_w = s1 + s3 + s2
        assert new_w == [0, 1, 2, 3, 5, 6, 4]

    def test_rot_inline(self):
        stack = [0, 1, 2, 3, 4, 5, 6]
        new_w = stack[0:-3] + stack[-2:] + stack[-3:-2]
        assert new_w == [0, 1, 2, 3, 5, 6, 4]

    def test_function_list(self):
        stack = []
        def plus(word, location):
            stack.append(stack.pop() + stack.pop())
            return 1

        def lit(word, location):
            stack.append(word[location + 1])
            return 2

        my_word = []
        word = 3
        my_word.append(lit)
        my_word.append(word)
        word = 4
        my_word.append(lit)
        my_word.append(word)
        my_word.append(plus)
        index = 0
        while index < len(my_word):
            function = my_word[index]
            increment = function(my_word, index)
            index += increment
        assert stack[0] == 7

    def test_function_list_lambda(self):
        # this version assumes only functions in the list
        stack = []

        my_list = [lambda : stack.append(3),
                   lambda : stack.append(4),
                   lambda : stack.append(stack.pop() + stack.pop())]

        for w in my_list:
            w()
        assert stack[0] == 7

    def test_function_list_lambda_temp(self):
        # this version assumes only functions in the list
        stack = []

        my_list = []
        word = 3
        my_list.append(lambda : stack.append(word))
        word = 4
        my_list.append(lambda : stack.append(word))
        my_list.append(lambda : stack.append(stack.pop() + stack.pop()))

        for w in my_list:
            w()
        assert stack[0] == 8 # not 7 as one might hope

