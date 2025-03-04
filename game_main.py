
import pygame



class Game:
    WHITE = (232, 232, 232)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    BASE_FONT = 'Courier New.ttf'
    GAME_XY = 800
    FORTH_SIZE = GAME_XY // 2
    WINDOW_SIZE = (GAME_XY + FORTH_SIZE, GAME_XY)
    BORDER = GAME_XY
    LEFT_MARGIN = 10
    BOTTOM_MARGIN = 20

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('ForthBots')
        self.lines = [
                'Forth> _',
                '4 ok',
                'Forth> 2 2 +',
                'alpha', 'bravo', 'charlie', 'delta', 'echo',
                'foxtrot', 'golf', 'hotel', 'india', 'juliett',
                'kilo', 'lima', 'mike', 'november',
                'oscar', 'papa', 'quebec', 'romeo', 'sierra',
                'tango', 'uniform', 'victor', 'whiskey', 'xray',
                'yankee', 'zulu'
            ]

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.lines.insert(0, 'Forth> _')
                    elif event.key == pygame.K_BACKSPACE:
                        self.lines[0] = self.lines[0][:-2] + '_'
                    else:
                        self.lines[0] = self.lines[0][:-1] + event.unicode + '_'
            self.screen.fill("midnightblue")
            pygame.draw.line(self.screen, self.WHITE,
                             (self.BORDER, 0),
                             (self.BORDER, self.GAME_XY), 1)
            rect = self.screen.get_rect()
            x = self.BORDER + self.LEFT_MARGIN
            y = rect.bottomleft[1] - self.BOTTOM_MARGIN
            for line in self.lines:
                self.text((x,y),line, 16, self.WHITE, "midnightblue")
                y -= 20
            pygame.display.flip()

    def text(self, location, phrase, size, front_color, back_color):
        font = pygame.font.Font(self.BASE_FONT, size)
        font.set_bold(True)
        text = font.render(phrase, True, front_color, back_color)
        text_rect = text.get_rect()
        text_rect.topleft = location
        self.screen.blit(text, text_rect)

if __name__ == '__main__':
    game = Game()
    game.main_loop()