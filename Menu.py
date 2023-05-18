import sys
import pygame
import SudokuGUI

pygame.init()

def main():
    screen = pygame.display.set_mode((630, 630))
    pygame.display.set_caption("Welcome to PyDoku!")

    font = pygame.font.SysFont("Arial", 36)

    title_label = font.render("Welcome to PyDoku!", True, (0, 0, 0))
    title_label_rect = title_label.get_rect(center=(315 , 100))

    quit_text = font.render("Quit", True, pygame.Color("black"))
    quit_rect = quit_text.get_rect(center=(70, 605))

    start_text = font.render("Start", True, pygame.Color("black"))
    start_rect = start_text.get_rect(center=(320, 300))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if 250 <= x <= 400 and 275 <= y <= 325:
                    print("Start button clicked!")
                    SudokuGUI.sudoku_loop()
                elif 0 <= x <= 150 and 580 <= y <= 630:
                    print("Quit button clicked!")
                    pygame.quit()
                    sys.exit()



        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, pygame.Color("gray"), pygame.Rect(250, 275, 150, 50), 0)
        pygame.draw.rect(screen, pygame.Color("gray"), pygame.Rect(0, 580, 150, 50), 0)
        screen.blit(title_label, title_label_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.update()



if __name__ == "__main__":
    main()
