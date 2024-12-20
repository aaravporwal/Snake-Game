import pygame
import time
import random
from pygame.locals import *

SIZE = 36

class Frog:
    def __init__(self, parent_screen):
        self.frog = pygame.image.load("frog.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.frog, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,15)*SIZE
        self.y = random.randint(0,10)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.snake = pygame.image.load("snake.jpg").convert()
        self.direction = 'down'

        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((80, 125, 42))
        for i in range(self.length):
            self.parent_screen.blit(self.snake, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
    def move_left(self):
       self.direction = 'left'
    def move_right(self):
        self.direction = 'right'

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -=SIZE
        if self.direction == 'down':
            self.y[0] +=SIZE
        if self.direction == 'left':
            self.x[0] -=SIZE
        if self.direction == 'right':
            self.x[0] +=SIZE
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((800, 732))
        self.surface.fill((80, 125, 42))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.frog = Frog(self.surface,)
        self.frog.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load("cat_bg_music.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("bg_image.jpg")
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.frog.draw()
        self.display_score()
        pygame.display.flip()
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.frog.x, self.frog.y):
            sound = pygame.mixer.Sound("ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.frog.move()

        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("crash.mp3")
                pygame.mixer.Sound.play(sound)
                raise("Game Over!")

    def display_score(self):
        font = pygame.font.SysFont('comic sans', 50)
        score = font.render(f"Score: {self.snake.length}", True, (200,200,200))
        self.surface.blit(score, (350,0))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('comic sans', 30)
        line1 = font.render(f"Game Over! Your Score is: {self.snake.length}", True, (200,200,200))
        self.surface.blit(line1, (150,300))

        line2 = font.render("To play again, press Enter. To exit, press Escape!", True, (200,200,200))
        self.surface.blit(line2, (150, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()
    def reset(self):
        self.render_background()
        self.snake = Snake(self.surface, 1)
        self.frog = Frog(self.surface, )


    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    pass
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.2)

if __name__=="__main__":
    pygame.init()
    game = Game()
    game.run()

