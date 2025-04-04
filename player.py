import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from shield import Shield


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, radius=PLAYER_RADIUS)
        self.rotation = 0
        self.x = x
        self.y = y
        self.shot_timer: float = 0
        self.mine_timer: float = 0
        self.shield_timer: float = 0
        self.teleport_timer: float = 0
        # self.image = pygame.image.load("images/player_image.png")
        # self.image_size = self.image.get_size()
        # self.sized_image = pygame.transform.scale(
        #     self.image, (int(self.image_size[0] / 35), int(self.image_size[1] / 35))
        # )

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        # screen.blit(self.sized_image, player_body)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt, dx=0, dy=0):
        self.shot_timer -= dt
        self.mine_timer -= dt
        self.shield_timer -= dt
        self.teleport_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_LSHIFT]:
            self.move(dt * 1.5)
        if keys[pygame.K_h]:
            self.shoot()
        if keys[pygame.K_k]:
            self.mine()
        if keys[pygame.K_j]:
            self.scatter_shot()
        if keys[pygame.K_l]:
            self.shield()
        if keys[pygame.K_g]:
            self.teleport()

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_timer > 0:
            return
        self.shot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(x=self.position.x, y=self.position.y, radius=SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED

    def mine(self):
        if self.mine_timer > 0:
            return
        self.mine_timer = PLAYER_MINE_COOLDOWN

        Shot(x=self.position.x, y=self.position.y, radius=MINE_RADIUS)

    def scatter_shot(self):
        if self.shot_timer > 0:
            return

        self.shot_timer = PLAYER_SCATTER_SHOT_COOLDOWN
        shot1 = Shot(x=self.position.x, y=self.position.y, radius=SHOT_RADIUS)
        shot2 = Shot(x=self.position.x, y=self.position.y, radius=SHOT_RADIUS)
        shot3 = Shot(x=self.position.x, y=self.position.y, radius=SHOT_RADIUS)
        shot1.velocity = (
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SCATTER_SHOT_SPEED
        )
        shot2.velocity = (
            pygame.Vector2(-0.25, 1).rotate(self.rotation) * PLAYER_SCATTER_SHOT_SPEED
        )
        shot3.velocity = (
            pygame.Vector2(0.25, 1).rotate(self.rotation) * PLAYER_SCATTER_SHOT_SPEED
        )

    def shield(self):
        if self.shield_timer > 0:
            return
        self.shield_timer = PLAYER_SHIELD_COOLDOWN

        shield = Shield(x=self.position.x, y=self.position.y, radius=SHIELD_RADIUS)
        shield.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * 0

    def teleport(self):
        if self.teleport_timer > 0:
            return
        self.teleport_timer = PLAYER_TELEPORT_COOLDOWN
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * 200
