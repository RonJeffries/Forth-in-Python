from source.forth import Forth
from source.keyboard_provider import KeyboardProvider

if __name__ == '__main__':
    # print(os.getcwd())
    forth = Forth()
    provider = KeyboardProvider(forth)
    while True:
        result = forth.main_loop(provider)
        if result != 'ok':
            provider.error(result)