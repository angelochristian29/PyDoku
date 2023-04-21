import sys
import pygame

import SudokuGUI

# initialize pygame
pygame.init()

# set window properties
screen_width = 630
screen_height = 630
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Welcome to PyDoku!")

# set font properties
font = pygame.font.SysFont("Arial", 36)

# create title label
title_label = font.render("Welcome to PyDoku!", True, (0, 0, 0))
title_label_rect = title_label.get_rect(center=(screen_width / 2, 100))

# create start button
start_button = font.render("Start", True, (0, 0, 0))
start_button_rect = start_button.get_rect(center=(screen_width / 2, 300))

# main loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                title_label = font.render("Welcome to e!", True, (0, 0, 0))
                SudokuGUI.sudoku_loop()


    # draw widgets
    screen.fill((255, 255, 255))
    screen.blit(title_label, title_label_rect)
    screen.blit(start_button, start_button_rect)

    # update display
    pygame.display.update()

    # check for mouse events
    mouse_pos = pygame.mouse.get_pos()
    if start_button_rect.collidepoint(mouse_pos):
        start_button = font.render("Start", True, (255, 0, 0))
    else:
        start_button = font.render("Start", True, (0, 0, 0))

    # draw start button
    screen.blit(start_button, start_button_rect)