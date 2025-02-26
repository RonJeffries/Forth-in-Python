from source.string_provider import StringProvider


class TestProviders:
    def test_string_provider(self):
        provider = StringProvider('abc def ghi')
        assert provider.has_tokens()
        assert provider.next_token() == 'ABC'
        assert provider.has_tokens()
        assert provider.next_token() == 'DEF'
        assert provider.has_tokens()
        assert provider.next_token() == 'GHI'