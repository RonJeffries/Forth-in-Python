from source.forth import Forth
import readline

if __name__ == '__main__':
    forth = Forth()
    prompt = 'Forth> '
    while True:
        foo = forth.find_word('FOO')
        line = input(prompt)
        if line == 'bye':
            break
        result = forth.safe_compile(line)
        prompt = 'Forth> '
        if result == '...':
            prompt = '...> '
        else:
            print(result)
