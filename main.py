import pygame
import time
from random import randint

pygame.init()

back = (200, 255, 255)
mw = pygame.display.set_mode((800, 600))
mw.fill(back)
clock = pygame.time.Clock()

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)

cards = []
num_cards = 4

x = 70

start_time = time.time()
cur_time = start_time

# Изменены координаты для текстовых меток и чисел
time_text = Label(20, 20, 50, 50, back)
time_text.set_text('Время:', 40, DARK_BLUE)
time_text.draw(0, 0)

timer = Label(150, 20, 50, 50, back)
timer.set_text('0', 40, DARK_BLUE)
timer.draw(0, 0)

score_text = Label(380, 20, 50, 50, back)
score_text.set_text('Счет:', 40, DARK_BLUE)
score_text.draw(0, 0)

score = Label(480, 20, 50, 50, back)
score.set_text('0', 40, DARK_BLUE)
score.draw(0, 0)

for i in range(num_cards):
    new_card = Label(x, 170, 100, 150, YELLOW)
    new_card.outline(BLUE, 10)
    new_card.set_text('CLICK', 26)
    cards.append(new_card)
    x = x + 120

wait = 0
point = 0

while True:
    if wait == 0:
        wait = 20
        click = randint(1, num_cards)
        for i in range(num_cards):
            cards[i].color(YELLOW)
            if (i + 1) == click:
                cards[i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                if cards[i].collidepoint(x, y):
                    if i + 1 == click:
                        cards[i].color(GREEN)
                        point += 1
                    else:
                        cards[i].color(RED)
                        point -= 1

                    cards[i].fill()
                    score.set_text(str(point), 40, DARK_BLUE)
                    score.draw(0, 0)

    new_time = time.time()
    if new_time - start_time >= 11:
        win = Label(0, 0, 800, 600, LIGHT_RED)
        win.set_text('Время вышло!', 60, DARK_BLUE)
        win.draw(200, 180)
        break
    if int(new_time) - int(cur_time) == 1:
        timer.set_text(str(int(new_time - start_time)), 40, DARK_BLUE)
        timer.draw(0, 0)
        cur_time = new_time
    if point >= 5:
        win = Label(0, 0, 800, 600, LIGHT_GREEN)
        win.set_text('Победа!', 60, DARK_BLUE)
        win.draw(340, 180)
        resul_time = Label(190, 250, 250, 250, LIGHT_GREEN)
        resul_time.set_text('Время прохождения: ' + str(int(new_time - start_time)) + ' сек', 40, DARK_BLUE)
        resul_time.draw(0, 0)
        break

    pygame.display.update()
    clock.tick(40)

# Цикл для ожидания закрытия окна
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Нажмите ESC для выхода
                pygame.quit()
                exit()
    pygame.display.update()
