import pygame
import random


def calculate_ground_height(window_height):
    return window_height * 7 // 8


class Ground:
    def __init__(self, window_width, window_height) -> None:
        self.x = 0
        self.y = calculate_ground_height(window_height)
        self.rectangle = pygame.Rect(self.x, self.y, window_width, 15)


    def draw(self, window):
        pygame.draw.rect(surface=window, color=(255, 255, 255), rect=self.rectangle)


class Pipes:
    def __init__(self, window_width, window_height) -> None:
        self.width = 45
        self.opening = 100
        self.ground_level = calculate_ground_height(window_height)
        self.opening_pixel_buffer = 10

        self.x = window_width
        self.bottom_height = random.randint(self.opening_pixel_buffer, self.ground_level - self.opening - self.opening_pixel_buffer)
        self.top_height = self.ground_level - self.bottom_height - self.opening
        self.bottom_rectangle = pygame.Rect(0, 0, 0, 0) # initialize for collision check
        self.top_rectangle = pygame.Rect(0, 0, 0, 0) # initialize for collision check
        self.passed = False
        self.off_screen = False
        self.color = (100, 200, 75)


    def draw(self, window):
        self.bottom_rectangle = pygame.Rect(self.x, self.ground_level - self.bottom_height, self.width, self.bottom_height)
        pygame.draw.rect(surface=window, color=self.color, rect=self.bottom_rectangle)

        self.top_rectangle = pygame.Rect(self.x, 0, self.width, self.top_height)
        pygame.draw.rect(surface=window, color=self.color, rect=self.top_rectangle)


    def update(self, bird_x_position = 128):
        self.x -= 1

        if self.x + self.width <= bird_x_position:
            self.passed = True

        if self.x <= -self.width:
            self.off_screen = True
