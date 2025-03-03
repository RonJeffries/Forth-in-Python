
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
            self.text((100,100), "Hello, World!", 16, self.WHITE, self.BLACK)
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