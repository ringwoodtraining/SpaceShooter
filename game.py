import pygame
import json

from operator import itemgetter

from actors import Asteroid, Spaceship
from utils import get_random_position, load_sprite, print_text, print_scores, ask, get_current_time

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 600

class GameObject:
    CURRENT_SCORE = 0
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = load_sprite("Space", False)
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.scores_list = []
        self.high_score = self._load()
        self.high_score_name = ""
        self.has_won = False
        self.time_stamp = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)

    def _reset_game(self):
        self.message = ""
        self.scores_list = []
        self.high_score_name = ""
        self.has_won = False
        self.time_stamp = ""
        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        self.main_menu()



    def _spawn_enemies(self):
        for _ in range(3):
            while True:
                position = get_random_position(self.screen)
                if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        self._spawn_enemies()
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def main_menu(self):
        title_font = pygame.font.SysFont("comicsans", 50)
        run = True
        while run:
            self.screen.blit(self.background, (0, 0))
            title_label = title_font.render("Press the mouse to begin...", True, (255, 255, 255))
            self.screen.blit(title_label, (SCREEN_WIDTH / 2 - title_label.get_width() / 2, 350))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.main_loop()
        pygame.quit()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                    self.spaceship
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_ESCAPE]:
                quit()
            if is_key_pressed[pygame.K_a]:  # left
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_d]:  # right
                self.spaceship.rotate(clockwise=True)
            if is_key_pressed[pygame.K_w]:  # up
                self.spaceship.accelerate()
            if is_key_pressed[pygame.K_s]:  # down
                self.spaceship.deaccelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    #self.spaceship = None
                    self.high_score_name = ask(self.screen, 200, 200, 170, 32)
                    self.time_stamp = get_current_time()
                    self.high_score.append([self.high_score_name, self.CURRENT_SCORE, self.time_stamp])
                    self._save(sorted(self.high_score, key=itemgetter(1), reverse=True))

                    for scores in self._load():
                        self.scores_list.append(scores)

                    self.message = "You lost!"
                    self._reset_game()
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.CURRENT_SCORE += 100
                    print(self.CURRENT_SCORE)
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if (not self.asteroids) and self.spaceship:
            if not self.has_won:
                self.high_score_name = ask(self.screen, 200, 200, 140, 32)
                self.time_stamp = get_current_time()
                self.high_score.append([self.high_score_name, self.CURRENT_SCORE, self.time_stamp])
                self._save(sorted(self.high_score, key=itemgetter(1), reverse=True))
                self.has_won = True

                for scores in self._load():
                    self.scores_list.append(scores)

            self.message = "You win!"
            self._reset_game()

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        if self.scores_list:
            for scores in range(5):
                print_scores(self.screen, self.screen.get_width()/2, self.screen.get_height()/1.7, scores, self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    def _load(self):
        try:
            with open("high_scores.json", "r") as file:
                highscores = json.load(file)  # Read the json file
        except FileNotFoundError:
            return []
        return sorted(highscores, key=itemgetter(1), reverse=True)

    def _save(self, highscores):
        with open("high_scores.json", "w") as file:
            json.dump(highscores, file)  # Write the list to the json file




