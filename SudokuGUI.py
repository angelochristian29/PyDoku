from SudokuBoard import SudokuBoard
import Menu
import sys, pygame as pg

buttons = {pg.K_1:1,pg.K_2:2,pg.K_3:3,pg.K_4:4,pg.K_5:5,pg.K_6:6,pg.K_7:7,pg.K_8:8,pg.K_9:9}
pg.init()
font = pg.font.SysFont(None, 60)
mySudoku = SudokuBoard()
mySudoku.s_board = mySudoku.sudoku_maker()


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

    def solve_draw(self, board, r, c, color):
        pg.draw.rect(self.canvas, pg.Color("white"), pg.Rect(c * 70 + 20, r * 70 + 20, 50, 50), 0)
        n_text = font.render(str(board[r][c]), True, pg.Color(color))
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
    def assign_number(self,position):
        if(position[0] > 630 or position[0] < 10 or position[1]>630 or position[1] < 10):
            return
        row = (position[1] - 10)//70
        col = (position[0] - 10)//70
        print(row,col)
        while(True):
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                        mySudoku.s_board[row][col] = buttons[event.key]
                        pg.display.flip()
                        pg.display.update()
                        return



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
    while to_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # to_run = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1 or event.key == pg.K_KP1:
                    myGUI.backtracking_solver(mySudoku.s_board, 0, 0)
                    if myGUI.board_finished():
                        print("Game Over")
            if event.type == pg.MOUSEBUTTONDOWN:
                myGUI.assign_number(pg.mouse.get_pos())
                x, y = pg.mouse.get_pos()
                if 475 <= x <= 625 and 670 <= y <= 720:
                    reset_game()
                if 300 <= x <= 450 and 670 <= y <= 720:
                    go_to_menu()
                if 125 <= x <= 275 and 670 <= y <= 720:
                    pg.quit()
                    sys.exit()

        myGUI.draw_canvas()
        myGUI.draw_nums(mySudoku.s_board)

        reset_text = font.render("Reset", True, pg.Color("black"))
        reset_rect = reset_text.get_rect(center=(550, 695))
        pg.draw.rect(canvas, pg.Color("gray"), pg.Rect(475, 670, 150, 50), 0)

        menu_text = font.render("Menu", True, pg.Color("black"))
        menu_rect = reset_text.get_rect(center=(375, 695))
        pg.draw.rect(canvas, pg.Color("gray"), pg.Rect(300, 670, 150, 50), 0)

        quit_text = font.render("Quit", True, pg.Color("black"))
        quit_rect = reset_text.get_rect(center=(200, 695))
        pg.draw.rect(canvas, pg.Color("gray"), pg.Rect(125, 670, 150, 50), 0)

        canvas.blit(reset_text, reset_rect)
        canvas.blit(menu_text, menu_rect)
        canvas.blit(quit_text, quit_rect)

        pg.display.flip()

# sudoku_loop()
# pg.quit()
