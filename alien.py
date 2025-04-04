import math
import pygame
from circleshape import CircleShape
from player import Player
from constants import *


class Alien(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=ALIEN_RADIUS)
        self.rotation = 0
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, "green", self.position, self.radius)

    def update(self, dt, dx=0, dy=0):
        self.position.x += dx
        self.position.y += dy
