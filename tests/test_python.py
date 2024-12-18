

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
