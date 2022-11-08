"""
ChromeDinoAI
Bhavya Muni
3/5/2020
"""


from dino import *
import pygame
from obstacle import *
import time


WIN_HEIGHT = 480
WIN_WIDTH = 640
MAX_TOT_WIDTH = 25*3
POPULATION = 10
dinos = []

best_score = 0







def main(dinos, gener, best_score):
    gen_score = 0
    cactus_vel = 14
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    font = pygame.font.SysFont("firacode", 24)
    scr = pygame.font.SysFont("firacode", 18)
    ground = Ground(cactus_vel)
    cacti = [Cactus(650, cactus_vel)]
    dead_dinos = []
    score = 0
    clock = pygame.time.Clock()

    while True:
        if len(dinos) == 0:
            gener += 1
            nextGen(gener, dead_dinos, gen_score, best_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        for dino in dinos:
            should_jump = dino.brain.think(cacti[0])[0]
            if should_jump > 0.5:
                dino.jump()

        if cacti[0].x <= cacti[0].count * (-cacti[0].CACTUS_IMG.get_width()):
            if len(dinos) > 0:
                gen_score += 1
            a = cacti.pop(0)
            del a
            cacti.append(Cactus(random.randint(650, 750), cactus_vel))

        ground.move()
        for dino in dinos:
            dino.move()
        for cactus in cacti:
            cactus.move()
            for i, dino in enumerate(dinos):
                if cactus.collide(dino):
                    dead = dinos.pop(i)
                    dead_dinos.append(dead)

        if cactus_vel < 18:
            cactus_vel += 0.02
        best_text = font.render(f"Best Score: {best_score}", True, (0, 0, 0))
        scores = [font.render(f"Score: {str(gen_score)}", True, (0, 0, 0)), font.render(
            f"Alive: {str(len(dinos))}", True, (0, 0, 0))]
        gen = font.render(f"Gen: {gener}", True, (0, 0, 0))
       
        # print(gen_score, " ", len(dinos))
        clock.tick(30)
        draw_window(screen, dinos, ground, cacti, gen, scores, best_text)


def draw_window(win, dinos, ground, cacti, score, scores, best):
    win.blit(pygame.image.load("./assets/white.jpg"), (0, 0))
    win.blit(score, (0, 0))
    win.blit(
        best, (WIN_WIDTH - scores[0].get_width() - best.get_width() - 20, 0))
    for i, j in enumerate(scores):
        win.blit(
            j, (WIN_WIDTH - scores[i].get_width(), i * scores[i].get_height()))
    ground.draw(win)
    for dino in dinos:
        dino.draw(win)
    for cactus in cacti:
        cactus.draw(win)
    pygame.display.update()


"""
GENETIC ALGORITHM
"""


def nextGen(gen, dead_dinos, score, best_score):
    new_dinos = []
    calcFitness(dead_dinos)
    if score > best_score:
        best_score = score
    for i in range(POPULATION):
        new_dinos.append(Dinosaur(pickDino(dead_dinos), peach))

    del dead_dinos
    main(new_dinos, gen, best_score)


def pickDino(dead_dinos):
    index = 0
    r = random.random()
    while r > 0:
        r = r - dead_dinos[index].fitness
        index += 1
    index -= 1
    dino = dead_dinos[index]
    new_dino_brain = Brain(dino.brain)
    new_dino_brain.mutate()
    return new_dino_brain


def calcFitness(dinos):
    total_score = sum((i.score for i in dinos))
    for dino in dinos:
        dino.fitness = dino.score/total_score


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)




def start_screen():
    



for i in range(POPULATION):
    dinos.append(Dinosaur(Brain(None), pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
gen = 1


main(dinos, gen, best_score)
