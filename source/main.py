from source.forth import Forth

if __name__ == '__main__':
    forth = Forth()
    prompt = 'Forth> '
    while True:
        line = input(prompt)
        if line == 'bye':
            break
        try:
            forth.compile(line)
            print('ok')
            prompt = 'Forth> '
        except Exception as e:
            if str(e) == 'Unexpected end of input':
                prompt = '...> '
            else:
                print(e, ' ?')
