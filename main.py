import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main() -> None:
    pygame.init()

    pygame.display.set_caption(title="Asteroids")

    font = pygame.font.SysFont(name="Comic Sans MS", size=100)

    points: int = 0
    points_text = font.render(str(points), False, (255, 255, 255))

    bg = pygame.image.load("background_image.jpg")
    asteroid_image = pygame.image.load("asteroid_image.png")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)

        for asteroid in asteroids:
            if player.check_collisions(other=asteroid):
                print("Game over!")
                sys.exit()

            for shot in shots:
                if shot.check_collisions(other=asteroid):
                    points += 1
                    shot.kill()
                    asteroid.split()

        screen.blit(bg, (0, 0))

        points_text = font.render(str(points), False, (255, 255, 255))
        screen.blit(points_text, (0, 0))

        for item in drawable:
            item.draw(screen)

        pygame.display.flip()

        dt: float = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
