from source.forth import Forth
import readline

if __name__ == '__main__':
    forth = Forth()
    prompt = 'Forth> '
    while True:
        result = forth.compile(input(prompt))
        if forth.compilation_state:
            prompt = '...'
        else:
            prompt = 'Forth> '
            print(result)
