import random
import pygame

from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound

from datetime import datetime

def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


def wrap_position(position, sprite, surface):
    x, y = position
    w, h = surface.get_size()

    if x < -sprite.get_width()/2:
        x = w + sprite.get_width()/2

    if x > w + sprite.get_width()/2:
        x = -sprite.get_width()/2

    if y < -sprite.get_height()/2:
        y = h + sprite.get_height()/2

    if y > h + sprite.get_height()/2:
        y = -sprite.get_height()/2

    return Vector2(x, y)


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, False, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)


def ask(screen, x, y, w, h):
    pygame.font.init()
    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''

    # create rectangle
    input_rect = pygame.Rect(x, y, w, h)

    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')

    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    color = color_passive

    active = False

    while True:
        for event in pygame.event.get():

            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]

                # Check for backspace
                if event.key == pygame.K_RETURN:
                    return user_text

                # Unicode standard is used for string formation
                else:
                    user_text += event.unicode

        if active:
            color = color_active
        else:
            color = color_passive

        # draw rectangle and argument passed which should be on screen
        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width() + 10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()


def get_current_time():
    current_date_time = datetime.now()
    return str(current_date_time)


def print_scores(surface, x, y, text, font, color=Color("tomato")):

    text_surface = font.render(str(text), False, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(x, y)
    surface.blit(text_surface, rect)