from source.compile_info import CompileInfo


class TestSys:
    def test_new_sys(self):
        sys = CompileInfo('CASE')
        assert sys.name == 'CASE'
        assert sys.locations == []