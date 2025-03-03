
import pygame



class Game:
    WHITE = (232, 232, 232)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    BASE_FONT = 'Courier New.ttf'

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('ForthBots')

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill("midnightblue")
            lines = [
                '4 ok',
                'Forth> 2 2 +',
                'alpha', 'bravo', 'charlie', 'delta', 'echo',
                'foxtrot', 'golf', 'hotel', 'india', 'juliett',
                'kilo', 'lima', 'mike', 'november',
                'oscar', 'papa', 'quebec', 'romeo', 'sierra',
                'tango', 'uniform', 'victor', 'whiskey', 'xray',
                'yankee', 'zulu'
            ]
            rect = self.screen.get_rect()
            y = rect.bottomleft[1] - 20
            for line in lines:
                self.text((10,y),line, 16, self.WHITE, "midnightblue")
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