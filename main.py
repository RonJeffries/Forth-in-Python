from source.forth import Forth
import readline

if __name__ == '__main__':
    forth = Forth()
    prompt = 'Forth> '
    while True:
        line = input(prompt)
        if line == 'bye':
            break
        result = forth.compile(line)
        prompt = 'Forth> '
        if result == '...':
            prompt = '...> '
        else:
            print(result)
