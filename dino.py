"""
ChromeDinoAI
Bhavya Muni
3/5/2020
"""

import os
import pygame

ASSETS_DIR = "./assets/run/"

WIN_HEIGHT = 480
WIN_WIDTH = 640


class Dinosaur:
    ANIMATION_TIME = 3
    IMGS = [
        pygame.image.load(os.path.join(ASSETS_DIR, i)) for i in os.listdir(ASSETS_DIR)
    ]
    IMGS = IMGS[:-2]
    IMGS = [
        pygame.transform.scale(i, (int(i.get_width() * 1.5), int(i.get_height() * 1.5)))
        for i in IMGS
    ]

    # IMGS = [i.set_alpha(100) for i in IMGS]

    VEL = 0

    def __init__(self, brain, color):
        self.color = color
        self.score = 0
        self.fitness = 0
        self.brain = brain
        self.x = 10
        self.y = WIN_HEIGHT - self.IMGS[0].get_height() - 2
        self.img_idx = 0
        self.image_count = 0
        self.image = self.IMGS[0]
        self.tick_count = 0
        self.die = False
        for img in self.IMGS:
            self.fill(img, self.color)

    def jump(self):
        if self.y == WIN_HEIGHT - self.IMGS[0].get_height() - 2:
            self.VEL = -15
            self.tick_count = 0

    def move(self):
        self.score += 1
        self.tick_count += 1
        d = self.tick_count * self.VEL + 1.75 * self.tick_count**2
        if d < 0:
            d -= 8
        self.y += d
        if self.y > WIN_HEIGHT - self.IMGS[0].get_height() - 2:
            self.y = WIN_HEIGHT - self.IMGS[0].get_height() - 2

    def animate(self):
        self.img_idx += 1
        if self.img_idx > len(self.IMGS) - 1:
            self.img_idx = 0

        self.image = self.IMGS[self.img_idx]

    def draw(self, win):
        self.image_count += 3
        if self.image_count % self.ANIMATION_TIME == 0:
            self.animate()
        win.blit(self.image, (self.x, self.y))

        # win.blit(self.get_mask(), (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    """
    Credit - skrx
    https://stackoverflow.com/a/42859550
    """

    def fill(self, surface, color):
        """Fill all pixels of the surface with color, preserve transparency."""
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))
