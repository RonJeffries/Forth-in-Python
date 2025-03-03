
import pygame

class Game:
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
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.main_loop()