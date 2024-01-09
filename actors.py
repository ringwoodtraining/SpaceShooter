import random

import pygame.transform
from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import get_random_velocity, load_sound, load_sprite, wrap_position

UP = Vector2(0, -1)


class Actor:
    def __init__(self, position, sprite, velocity, direction):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.direction = Vector2(direction)

    def rotate(self, angle):
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, self.sprite, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)

        return distance < self.radius + other_obj.radius

    def scale(self, scale):
        self.radius = self.radius * scale
        self.sprite = pygame.transform.scale_by(self.sprite, (scale, scale))


class Spaceship(Actor):
    MANEUVERABILITY = 6
    ACCELERATION = 0.25
    BULLET_SPEED = 6

    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite("spaceship"), Vector2(0), self.direction)

        self.scale(0.25)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def deaccelerate(self):
        self.velocity -= self.direction * self.ACCELERATION

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet_direction = self.direction
        bullet = Bullet(self.position, bullet_velocity, bullet_direction)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()


class Asteroid(Actor):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("VirusBigPack/png" + str(random.randint(1, 114))), 0, scale)
        super().__init__(position, sprite, get_random_velocity(1, 3), UP)

        self.scale(0.25)

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)


class Bullet(Actor):
    def __init__(self, position, velocity, angle):
        super().__init__(position, load_sprite("bullet"), velocity, angle)
        self.scale(0.15)

    def move(self, surface):
        self.position = self.position + self.velocity
