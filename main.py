import os
import sys
import pygame
import time
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from shield import Shield
from highscore import save_highscore, read_highscore
from best_time import save_best_time, read_best_time


def main() -> None:
    pygame.init()

    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    bg_image_path = os.path.join(base_path, "images", "background_image.jpg")
    bg = pygame.image.load(bg_image_path)

    pygame.display.set_caption(title="Asteroids")

    title_font = pygame.font.SysFont(name="Comic Sans MS", size=200)
    points_font = pygame.font.SysFont(name="Comic Sans MS", size=50)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    shields = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Shield.containers = (shields, updatable, drawable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    AsteroidField()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    )
    points: int = 0
    highscore: str = read_highscore()
    collision: bool = False
    shield_health: int = 3
    start_time = time.time()
    best_time = read_best_time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            break
        if pygame.key.get_pressed()[pygame.K_q]:
            sys.exit()

        screen.blit(bg, (0, 0))

        title = title_font.render("ASTEROIDS", False, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH / 5.5, SCREEN_HEIGHT / 5))

        title = points_font.render("PRESS SPACE TO START", False, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))

        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        for asteroid in asteroids:
            if player.check_collisions(other=asteroid):
                if points > int(highscore):
                    save_highscore(points)

                if time.time() - start_time > float(best_time):
                    save_best_time(round(float(time.time() - start_time), 2))

                collision = True

            for shot in shots:
                if shot.check_collisions(other=asteroid):
                    points += 1
                    shot.kill()
                    asteroid.split()

            for shield in shields:
                if shield.check_collisions(other=asteroid):
                    points += 1
                    if shield_health < 2:
                        shield.kill()
                        shield_health = 4

                    asteroid.split()
                    shield_health -= 1

        if collision:
            break

        screen.blit(bg, (0, 0))

        time_text = points_font.render(
            "Time: " + str(round(time.time() - start_time, 2)), False, (255, 255, 255)
        )
        screen.blit(time_text, (0, 150))

        best_time_text = points_font.render(
            "Best Time: " + best_time, False, (255, 255, 255)
        )
        screen.blit(best_time_text, (0, 100))

        highscore_text = points_font.render(
            "Highscore: " + str(highscore), False, (255, 215, 0)
        )
        screen.blit(highscore_text, (0, 0))

        points_text = points_font.render(
            "Points: " + str(points), False, (155, 155, 155)
        )
        screen.blit(points_text, (0, 50))

        updatable.update(dt)

        for item in drawable:
            item.draw(screen)

        pygame.display.flip()

        dt: float = clock.tick(60) / 1000

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            main()
        if pygame.key.get_pressed()[pygame.K_q]:
            sys.exit()

        screen.blit(bg, (0, 0))

        title = title_font.render("GAME OVER!", False, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH / 6.5, SCREEN_HEIGHT / 6))

        title = points_font.render("PRESS SPACE TO PLAY AGAIN", False, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH / 3.5, SCREEN_HEIGHT / 2))

        pygame.display.flip()


if __name__ == "__main__":
    main()
