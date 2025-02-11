from source.forth import Forth


class TestCase:
    def test_hookup(self):
        assert True

    def test_trivial_case(self):
        f = Forth()
        f.process_line(': TEST 3 CASE ENDCASE ;')
        w = f.find_word('TEST')
        words = w.words
        assert str(w) == ': TEST *# 3 DROP ;'

