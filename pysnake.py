#!/usr/bin/env python

""" Simple 'snake' game implementation using pygame """

import pygame
import random
from pygame.locals import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_ESCAPE, KEYUP, QUIT

# Constants
WINSIZE = [640, 640]
WINCENTER = [320, 320]
INITIAL_SIZE = 3
INITIAL_SPEED = 10
PART_SIZE = 10

# Colors
WHITE = 255, 240, 200
BLACK = 0, 0, 0
RED = 255, 0, 0

# Directions
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3


def random_pos(width=WINSIZE[0], height=WINSIZE[1]):
    return (
        random.randint(0, width/10)*10,
        random.randint(0, height/10)*10
    )


class Apple:

    def __init__(self, color=RED):
        self.x, self.y = random_pos()
        self.surface = pygame.Surface((PART_SIZE, PART_SIZE))
        self.surface.fill(color)
        self.eaten = False

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


class SnakeBodyPart:

    def __init__(self, x, y, color=WHITE):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((PART_SIZE, PART_SIZE))
        self.surface.fill(color)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


class Snake:

    def __init__(self, x, y, color=WHITE):
        self.color = color
        self.speed = INITIAL_SPEED
        self.direction = LEFT

        self.body = list()
        for i in range(INITIAL_SIZE):
            self.body.append(SnakeBodyPart(x, y, color))
            x += PART_SIZE

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)

    def grow(self):
        tail = self.body[-1]
        self.body.append(SnakeBodyPart(tail.x, tail.y))

    def check_collision(self):
        for part in self.body[1:]:
            if self.body[0].x == part.x and self.body[0].y == part.y:
                return True
        return False

    def eat(self, apple):
        if self.body[0].x == apple.x and self.body[0].y == apple.y:
            apple.eaten = True
            self.grow()

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y
        if self.direction == LEFT:
            self.body[0].x -= self.speed
        elif self.direction == UP:
            self.body[0].y -= self.speed
        elif self.direction == RIGHT:
            self.body[0].x += self.speed
        elif self.direction == DOWN:
            self.body[0].y += self.speed

    def change_direction(self, button):
        if button == K_LEFT:
            if self.direction is not RIGHT:
                self.direction = LEFT
        elif button == K_RIGHT:
            if self.direction is not LEFT:
                self.direction = RIGHT
        elif button == K_DOWN:
            if self.direction is not UP:
                self.direction = DOWN
        elif button == K_UP:
            if self.direction is not DOWN:
                self.direction = UP


def main():
    # initialize and prepare screen
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('PySnake')
    screen.fill(BLACK)

    snake = Snake(WINCENTER[0], WINCENTER[1])
    apple = Apple()

    # Main game loop
    done = 0
    while not done:
        clock.tick(20)
        if apple.eaten:
            apple = Apple()
        apple.draw(screen)
        snake.draw(screen)
        snake.move()
        snake.eat(apple)
        if snake.check_collision():
            done = 1
            break
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                done = 1
                break
            if (e.type == KEYUP and
                (e.key == K_LEFT or e.key == K_RIGHT or
                 e.key == K_DOWN or e.key == K_UP)):
                snake.change_direction(e.key)
        pygame.display.update()
        screen.fill(BLACK)


if __name__ == '__main__':
    main()
