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
POPULATION = 7
dinos = []

peach = pygame.Color(255, 118, 95)

for i in range(POPULATION):
    dinos.append(Dinosaur(Brain(None), peach))
gen = 1


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
        clock.tick(30)
        print(gen_score, " ", len(dinos))
        if best_score >= 7:
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
    new_dino_brain.mutate(0.15)
    return new_dino_brain


def calcFitness(dinos):
    total_score = sum([dinos[i].score for i in range(len(dinos))])
    for dino in dinos:
        dino.fitness = dino.score/total_score


main(dinos, gen, best_score)
