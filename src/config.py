import pygame
import components


window_width = 720
window_height = 720

window = pygame.display.set_mode(size=(window_width, window_height))
ground = components.Ground(window_width, window_height)
pipes = []
