import pygame
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x: int, y: int, radius: int) -> None:
        super().__init__(x, y, radius)
        self.radius: int = radius

    def draw(self, screen) -> None:
        pygame.draw.circle(
            surface=screen,
            color="white",
            center=self.position,
            radius=self.radius,
            width=2,
        )

    def update(self, dt) -> None:
        self.position += self.velocity * dt
