import sys
import pygame

import SudokuGUI

# initialize pygame
pygame.init()

def main():
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

    # create quit button objects
    quit_button = font.render("Quit", True, (0, 0, 0))
    quit_button_rect = quit_button.get_rect(bottomleft=(10, screen_height-10))

    # main loop
    while True:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    print("Start button clicked!")
                    SudokuGUI.sudoku_loop()
                elif quit_button_rect.collidepoint(event.pos):
                    print("Quit button clicked!")
                    pygame.quit()
                    sys.exit()

        # draw widgets
        screen.fill((255, 255, 255))
        screen.blit(title_label, title_label_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(quit_button, quit_button_rect)

        # update display
        pygame.display.update()

        # check for mouse events
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            start_button = font.render("Start", True, (255, 0, 0))
        else:
            start_button = font.render("Start", True, (0, 0, 0))

        if quit_button_rect.collidepoint(mouse_pos):
            quit_button = font.render("Quit", True, (255, 0, 0))
        else:
            quit_button = font.render("Quit", True, (0, 0, 0))

if __name__ == "__main__":
    main()