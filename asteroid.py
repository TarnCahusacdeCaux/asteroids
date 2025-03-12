import pygame
import random
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x: int, y: int, radius: int) -> None:
        super().__init__(x, y, radius)
        self.image = pygame.image.load("asteroid_image.png")

    def draw(self, screen) -> None:
        image_size = self.image.get_size()

        if self.radius >= ASTEROID_MAX_RADIUS:
            sized_image = pygame.transform.scale(
                self.image, (int(image_size[0] // 2), int(image_size[1] // 2))
            )
            image_position = (
                self.position[0] - 75,
                self.position[1] - 65,
                self.position[0] - 75,
                self.position[1] - 65,
            )
        elif self.radius <= ASTEROID_MIN_RADIUS:
            sized_image = pygame.transform.scale(
                self.image, (int(image_size[0] / 6), int(image_size[1] / 6))
            )
            image_position = (
                self.position[0] - 30,
                self.position[1] - 20,
                self.position[0] - 30,
                self.position[1] - 20,
            )
        else:
            sized_image = pygame.transform.scale(
                self.image, (int(image_size[0] // 3), int(image_size[1] // 3))
            )
            image_position = (
                self.position[0] - 50,
                self.position[1] - 40,
                self.position[0] - 50,
                self.position[1] - 40,
            )
        screen.blit(sized_image, image_position)

    def update(self, dt) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle: float = random.uniform(a=20, b=50)
        vector1 = self.velocity.rotate(random_angle)
        vector2 = self.velocity.rotate(-random_angle)

        new_radius: int = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(x=self.position.x, y=self.position.y, radius=new_radius)
        asteroid2 = Asteroid(x=self.position.x, y=self.position.y, radius=new_radius)
        asteroid1.velocity = vector1 * 1.2
        asteroid2.velocity = vector2 * 1.2
