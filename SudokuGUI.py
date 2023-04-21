from SudokuSolver.SudokuBoard import SudokuBoard
import sys, pygame as pg

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
            pg.draw.line(self.canvas, pg.Color("black"), pg.Vector2((i * 70) + 10, 10), pg.Vector2((i * 70) + 10, 640), line_width)
            pg.draw.line(self.canvas, pg.Color("black"), pg.Vector2(10, (i * 70) + 10), pg.Vector2(640, (i * 70) + 10), line_width)
            i += 1
        if self.board_finished():
            n_text = font.render("Game Over", True, pg.Color("black"))
            self.canvas.blit(n_text, pg.Vector2(210, 680))

    def draw_nums(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    n_text = font.render(str(board[r][c]), True, pg.Color("black"))
                    self.canvas.blit(n_text, pg.Vector2((c * 70) + 33.5, (r * 70) + 27.5)) # modify this for sketching feature

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

# main
def sudoku_loop():
    canvas_size = 650, 750
    canvas = pg.display.set_mode(canvas_size)
    pg.display.set_caption("Sudoku Solver")
    to_run = True
    myGUI = SudokuGUI(canvas)
    while to_run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                to_run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1 or event.key == pg.K_KP1:
                    myGUI.backtracking_solver(mySudoku.s_board, 0, 0)
                    if myGUI.board_finished():
                        print("Game Over")
        myGUI.draw_canvas()
        myGUI.draw_nums(mySudoku.s_board)
        pg.display.flip()


sudoku_loop()
pg.quit()
