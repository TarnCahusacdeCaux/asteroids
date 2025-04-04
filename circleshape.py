import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius: int = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt, dx=0, dy=0):
        # sub-classes must override
        pass

    def check_collisions(self, other) -> bool:
        return self.position.distance_to(other.position) <= self.radius + other.radius
