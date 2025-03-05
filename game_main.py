import sys
from io import StringIO

import pygame

from source.forth import Forth


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
        self.forth = Forth()
        self.running = False
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('ForthBots')
        self.lines = [
                'Forth> _'
            ]

    def call_forth(self, line):
        original_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            result = self.forth.compile(line)
        finally:
            sys.stdout = original_stdout
        return captured_output.getvalue() + result

    def main_loop(self):
        self.running = True
        while self.running:
            self.process_events()
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

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.process_keystroke(event)

    def process_keystroke(self, event):
        if event.key == pygame.K_RETURN:
            self.append_forth_result()
            self.lines.insert(0, 'Forth> _')
        elif event.key == pygame.K_BACKSPACE:
            self.lines[0] = self.lines[0][:-2] + '_'
        else:
            self.lines[0] = self.lines[0][:-1] + event.unicode + '_'

    def append_forth_result(self):
        self.lines[0] = self.lines[0][:-1]
        forth_line = self.lines[0][6:]
        result = self.call_forth(forth_line)
        result_lines = result.split('\n')
        for line in result_lines:
            self.lines.insert(0, line)

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