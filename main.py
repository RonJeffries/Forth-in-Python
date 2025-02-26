from source.forth import Forth
import readline

from source.keyboard_provider import KeyboardProvider

if __name__ == '__main__':
    forth = Forth()
    provider = KeyboardProvider(forth)
    forth.main_loop(provider)
