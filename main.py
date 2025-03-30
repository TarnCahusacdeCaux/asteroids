import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from highscore import save_highscore, read_highscore


def main() -> None:
    pygame.init()

    pygame.display.set_caption(title="Asteroids")

    font = pygame.font.SysFont(name="Comic Sans MS", size=50)

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
    points: int = 0
    highscore: str = read_highscore()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if player.check_collisions(other=asteroid):
                if points > int(highscore):
                    save_highscore(points)

                print("Game over!")
                sys.exit()

            for shot in shots:
                if shot.check_collisions(other=asteroid):
                    points += 1
                    shot.kill()
                    asteroid.split()

        screen.blit(bg, (0, 0))

        highscore_text = font.render(
            "Highscore: " + str(highscore), False, (255, 215, 0)
        )
        screen.blit(highscore_text, (0, 0))

        points_text = font.render("Points: " + str(points), False, (155, 155, 155))
        screen.blit(points_text, (0, 50))

        for item in drawable:
            item.draw(screen)

        pygame.display.flip()

        dt: float = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
