"""
ChromeDinoAI
Bhavya Muni
3/5/2020
"""

import pygame
import numpy
import random

WIN_HEIGHT = 480
WIN_WIDTH = 640


class Cactus:
    CACTUS_IMG = pygame.image.load("./assets/cactus_large.png")
    CACTUS_IMG_2 = pygame.image.load("./assets/cactus_small.png")
    CACTUS_IMG = pygame.transform.scale(CACTUS_IMG,
                                        (int(CACTUS_IMG.get_width()*1.5), int(CACTUS_IMG.get_height() * 1.5)))
    CACTUS_IMG_2 = pygame.transform.scale(CACTUS_IMG_2,
                                          (int(CACTUS_IMG_2.get_width()*1.5), int(CACTUS_IMG_2.get_height() * 1.5)))

    CACTUS_IMGS = [CACTUS_IMG, CACTUS_IMG_2]

    def __init__(self, x, vel):
        self.VEL = vel
        self.x = x
        self.count = random.randint(1, 3)
        self.rand = [random.randint(0, 1) for i in range(self.count)]
        self.IMG_ARR = [self.CACTUS_IMGS[i] for i in self.rand]
        self.y = [WIN_HEIGHT - i.get_height()-2 for i in self.IMG_ARR]
        self.total_width = self.IMG_ARR[-1].get_width()
        self.widths = [self.x]
        for i in self.IMG_ARR[:-1]:
            self.widths.append(self.x + i.get_width())
            self.total_width += i.get_width()
        self.cactus_masks = [pygame.mask.from_surface(i) for i in self.IMG_ARR]

    def move(self):
        self.x -= self.VEL
        self.widths = [i - self.VEL for i in self.widths]

    def draw(self, win):
        curr_width = self.x

        for i, j in enumerate(self.IMG_ARR):
            win.blit(
                j, (curr_width, self.y[i]))
            curr_width += j.get_width()

    def collide(self, dino):
        dino_mask = dino.get_mask()
        dino.die = True
        for i in range(self.count):
            offset = (round(self.widths[i] - dino.x), self.y[i] -
                      round(dino.y) + round(self.IMG_ARR[i].get_height() / 2))
            if(dino_mask.overlap(self.cactus_masks[i], offset)):
                return True
        return False


class Ground:
    GROUND_IMG = pygame.image.load("./assets/ground.png")
    GROUND_IMG = pygame.transform.scale(GROUND_IMG,
                                        (int(GROUND_IMG.get_width()*1.5), int(GROUND_IMG.get_height() * 1.5)))

    def __init__(self, vel):
        self.VEL = vel
        self.GROUND_IMG.convert()
        self.y = WIN_HEIGHT - self.GROUND_IMG.get_height()-2
        self.x = 0
        self.x2 = self.GROUND_IMG.get_width()
        self.displacement = 0
        self.anim_wait_count = 0

    def move(self):
        self.x -= self.VEL
        self.x2 -= self.VEL
        if self.x + self.GROUND_IMG.get_width() < 0:
            self.x = self.x2 + self.GROUND_IMG.get_width()
        if self.x2 + self.GROUND_IMG.get_width() < 0:
            self.x2 = self.x + self.GROUND_IMG.get_width()

    def draw(self, win):
        win.blit(self.GROUND_IMG, (self.x, self.y))
        win.blit(self.GROUND_IMG, (self.x2, self.y))
