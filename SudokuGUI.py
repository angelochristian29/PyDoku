import os

import Menu
from SudokuBoard import SudokuBoard
import SudokuCSP
import Menu
import sys, pygame as pg
import time

buttons = {pg.K_1:1,pg.K_2:2,pg.K_3:3,pg.K_4:4,pg.K_5:5,pg.K_6:6,pg.K_7:7,pg.K_8:8,pg.K_9:9}
pg.init()
font = pg.font.SysFont(None, 60)
mySudoku = SudokuBoard()
mySudoku.s_board = mySudoku.sudoku_maker()

class Timer():
    started = False
    start = 0
    def timer():
        if(Timer.started):
            Timer.started = False
            return time.time() - Timer.start
        else:
            Timer.start = time.time()
            Timer.started = True
        
class SudokuGUI:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_canvas(self):
        self.canvas.fill(pg.Color("white"))
        pg.draw.rect(self.canvas, pg.Color("black"), pg.Rect(10, 10, 630, 630), 10)
        i = 1
        while i * 70 < 630:
            line_width = 3 if i % 3 > 0 else 8
            pg.draw.line(self.canvas, pg.Color("black"), pg.Vector2((i * 70) + 10, 10), pg.Vector2((i * 70) + 10, 640),
                         line_width)
            pg.draw.line(self.canvas, pg.Color("black"), pg.Vector2(10, (i * 70) + 10), pg.Vector2(640, (i * 70) + 10),
                         line_width)
            i += 1
        if self.board_finished():
            n_text = font.render("Game Over", True, pg.Color("black"))
            self.canvas.blit(n_text, pg.Vector2(210, 680))

    def draw_nums(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    n_text = font.render(str(board[r][c]), True, pg.Color("black"))
                    self.canvas.blit(n_text,
                                     pg.Vector2((c * 70) + 33.5, (r * 70) + 27.5))  # modify this for sketching feature
    def draw_nums_CSP(self,board):
        for r in range(9):
            for c in range(9):
                if board.board[r][c].value.get() != 0:
                    n_text = font.render(str(board.board[r][c].value.get()), True, pg.Color("black"))
                    self.canvas.blit(n_text,
                                     pg.Vector2((c * 70) + 33.5, (r * 70) + 27.5))  # modify this for sketching feature

    def solve_draw(self, board, r, c, color):
        pg.draw.rect(self.canvas, pg.Color("white"), pg.Rect(c * 70 + 20, r * 70 + 20, 50, 50), 0)
        n_text = font.render(str(board.board[r][c].value.get()), True, pg.Color(color))
        self.canvas.blit(n_text, pg.Vector2((c * 70) + 33.5, (r * 70) + 27.5))

    def backtracking_solver(self, board, r, c):
        if r > mySudoku.side - 1:
            return True
        if board[r][c] != 0:
            if c == mySudoku.side - 1:
                itr = self.backtracking_solver(board, r + 1, 0)
            else:
                itr = self.backtracking_solver(board, r, c + 1)
            return itr
        else:
            for i in range(1, mySudoku.side + 1):
                if mySudoku.is_present(board, r, c, i):
                    board[r][c] = i
                    self.solve_draw(board, r, c, "blue")
                    pg.display.flip()
                    pg.display.update()
                    pg.time.delay(15)
                    if c == mySudoku.side - 1:
                        itr = self.backtracking_solver(board, r + 1, 0)
                    else:
                        itr = self.backtracking_solver(board, r, c + 1)
                    if itr is True:
                        return True
            board[r][c] = 0
            self.solve_draw(board, r, c, "red")
            pg.display.flip()
            pg.display.update()
            pg.time.delay(15)
            return False

    def board_finished(self):
        for r in range(mySudoku.side):
            for c in range(mySudoku.side):
                if mySudoku.s_board[r][c] == 0:
                    return False
        return True
    # def assign_number(self,position):
    #     if(position[0] > 630 or position[0] < 10 or position[1]>630 or position[1] < 10):
    #         return
    #     row = (position[1] - 10)//70
    #     col = (position[0] - 10)//70
    #     print(row,col)
    #     while(True):
    #         for event in pg.event.get():
    #             if event.type == pg.KEYDOWN:
    #                     mySudoku.s_board[row][col] = buttons[event.key]
    #                     pg.display.flip()
    #                     pg.display.update()
    #                     return

def update(GUI,board,r,c,color):
    GUI.solve_draw(board, r, c, color)
    pg.display.flip()
    pg.display.update()
    #pg.time.delay(15)
# main
def reset_game():
    global mySudoku
    mySudoku = SudokuBoard()
    mySudoku.s_board = mySudoku.sudoku_maker()


def go_to_menu():
    Menu.main()


def sudoku_loop():
    canvas_size = 650, 750
    canvas = pg.display.set_mode(canvas_size)

    pg.display.set_caption("Sudoku Solver")
    to_run = True
    myGUI = SudokuGUI(canvas)
    GUIAdapter = SudokuCSP.CSPGUIAdapter(myGUI,"blue",update)
    simple_board = SudokuBoard().sudoku_maker()
    board = SudokuCSP.Board(simple_board,GUIAdapter)
    while to_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # to_run = False
                pg.quit()
                sys.exit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_1 or event.key == pg.K_KP1:
            #         Timer.timer()
            #         board.backtracking_search()
            #         print(Timer.timer())
            #         if myGUI.board_finished():
            #             print("Game Over")
            if event.type == pg.MOUSEBUTTONDOWN:
                # myGUI.assign_number(pg.mouse.get_pos())
                x, y = pg.mouse.get_pos()
                if 486 <= x <= 611 and 670 <= y <= 720:
                    simple_board = SudokuBoard().sudoku_maker()
                    board = SudokuCSP.Board(simple_board,GUIAdapter)
                if 329 <= x <= 454 and 670 <= y <= 720:
                    go_to_menu()
                if 172 <= x <= 295 and 670 <= y <= 720:
                    pg.quit()
                    sys.exit()
                if 15 <= x <= 140 and 670 <= y <= 720:
                    Timer.timer()
                    board.backtracking_search()
                    print(Timer.timer())
                    if myGUI.board_finished():
                        print("Game Over")

        myGUI.draw_canvas()
        myGUI.draw_nums_CSP(board)

        width = 125
        height = 50

        reset_text = font.render("Reset", True, pg.Color("black"))
        reset_rect = reset_text.get_rect(center=(486+(width/2), 695))
        pg.draw.rect(canvas, pg.Color("gray"), pg.Rect(486, 670, width, height), 0)

        menu_text = font.render("Menu", True, pg.Color("black"))
        menu_rect = reset_text.get_rect(center=(329+(width/2), 695))
        pg.draw.rect(canvas, pg.Color("gray"), pg.Rect(329, 670, width, height), 0)

        quit_text = font.render("Quit", True, pg.Color("black"))
        quit_rect = reset_text.get_rect(center=(180+(width/2), 695))
        pg.draw.rect(canvas, pg.Color("gray"), pg.Rect(172, 670, width, height), 0)

        solve_text = font.render("Solve", True, pg.Color("black"))
        solve_rect = solve_text.get_rect(center=(15+(width/2), 695))
        pg.draw.rect(canvas, pg.Color("gray"), pg.Rect(15, 670, width, height), 0)

        canvas.blit(reset_text, reset_rect)
        canvas.blit(menu_text, menu_rect)
        canvas.blit(quit_text, quit_rect)
        canvas.blit(solve_text, solve_rect)
        pg.display.flip()
#sudoku_loop()
#pg.quit()
