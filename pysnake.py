#!/usr/bin/env python
""" Simple snake game implementation using pygame """

import pygame
import random
from pygame.locals import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_ESCAPE, KEYUP, QUIT


class Apple:
    APPLE_SIZE = 10

    def __init__(self, position, color):
        self.x, self.y = position
        self.surface = pygame.Surface((self.APPLE_SIZE, self.APPLE_SIZE))
        self.surface.fill(color)
        self.eaten = False

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


class SnakeBodyPart:
    def __init__(self, position, color, size):
        self.x, self.y = position
        self.surface = pygame.Surface((size, size))
        self.surface.fill(color)

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))


class Snake:

    SNAKE_SIZE = 3
    SNAKE_SPEED = 10
    SNAKE_PART_SIZE = 10
    GROW_SPEED = 5

    # Directions
    LEFT, UP, RIGHT, DOWN = range(4)

    def __init__(self, position, color):
        self.color = color
        self.speed = self.SNAKE_SPEED
        self.direction = self.LEFT

        self.body = list()
        position = list(position)  # So we can increment X
        for i in range(self.SNAKE_SIZE):
            self.body.append(SnakeBodyPart(position, color, self.SNAKE_PART_SIZE))
            position[
                0
            ] += (
                self.SNAKE_PART_SIZE
            )  # Increment X so the snake starts as a horizontal line

    def head_position(self):
        return (self.body[0].x, self.body[1].y)

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)

    def grow(self):
        tail = self.body[-1]
        for _ in range(self.GROW_SPEED):
            self.body.append(
                SnakeBodyPart((tail.x, tail.y), self.color, self.SNAKE_PART_SIZE)
            )

    def check_collision(self):
        for part in self.body[1:]:
            if self.body[0].x == part.x and self.body[0].y == part.y:
                return True
        return False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        if self.direction == self.LEFT:
            self.body[0].x -= self.speed
        elif self.direction == self.UP:
            self.body[0].y -= self.speed
        elif self.direction == self.RIGHT:
            self.body[0].x += self.speed
        elif self.direction == self.DOWN:
            self.body[0].y += self.speed

    def change_direction(self, button):
        if button == K_LEFT:
            if self.direction is not self.RIGHT:
                self.direction = self.LEFT
        elif button == K_RIGHT:
            if self.direction is not self.LEFT:
                self.direction = self.RIGHT
        elif button == K_DOWN:
            if self.direction is not self.UP:
                self.direction = self.DOWN
        elif button == K_UP:
            if self.direction is not self.DOWN:
                self.direction = self.UP


class Game:
    # Game configurations
    WINDOW_SIZE = [640, 640]
    BACKGROUND_COLOR = 0, 0, 0  # Black
    SNAKE_COLOR = 255, 255, 255  # White
    APPLE_COLOR = 255, 0, 0  # Red

    MOVEMENT_KEYS = [K_LEFT, K_RIGHT, K_DOWN, K_UP]

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PySnake")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.screen.fill(self.BACKGROUND_COLOR)

        self.spawn_snake()
        self.spawn_apple()

    @property
    def window_center(self):
        return (self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[1] / 2)

    def random_window_coordinates(self):
        return (
            random.randint(0, self.WINDOW_SIZE[0] / 10) * 10,
            random.randint(0, self.WINDOW_SIZE[1] / 10) * 10,
        )

    def spawn_apple(self):
        self.apple = Apple(self.random_window_coordinates(), self.APPLE_COLOR)

    def spawn_snake(self):
        self.snake = Snake(self.window_center, self.SNAKE_COLOR)

    def run(self):
        done = False
        while not done:
            self.clock.tick(20)

            self.check_if_apple_was_eaten()
            if self.check_collision():
                done = True
                break

            # Capture events and change positions
            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                    done = True
                    break
                if e.type == KEYUP and e.key in self.MOVEMENT_KEYS:
                    self.snake.change_direction(e.key)
            self.snake.move()

            # Draw and update things on the screen
            self.draw()
            pygame.display.update()
            self.screen.fill(self.BACKGROUND_COLOR)

    def draw(self):
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)

    def is_position_out_of_screen(self, position):
        x = position[0]
        y = position[1]
        return x < 0 or x > self.WINDOW_SIZE[0] or y < 0 or y > self.WINDOW_SIZE[1]

    def check_collision(self):
        collision = False
        # Check if snake colide with itself
        collision |= self.snake.check_collision()
        # Check if snake colide with window borders
        collision |= self.is_position_out_of_screen(self.snake.head_position())
        return collision

    def check_if_apple_was_eaten(self):
        x, y = self.snake.head_position()
        if x == self.apple.x and y == self.apple.y:
            self.apple.eaten = True
            self.snake.grow()
            self.spawn_apple()


def main():
    game = Game()
    game.run()
    print("Game Over")


if __name__ == "__main__":
    main()
