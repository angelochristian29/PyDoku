from SudokuCSP import *
from SudokuBoard import *
from SudokuGUI import *


def test_board(test_board):
    print("Before\n" + str(test_board))
    test_board.arc_inference()
    test_board.backtracking_search()
    print("After\n" + str(test_board))


def main():
    board = Board(
        [[0, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0],
         [0, 0, 8, 1, 0, 2, 9, 0, 0],
         [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0], [0, 0, 2, 6, 0, 9, 5, 0, 0],
         [8, 0, 0, 2, 0, 3, 0, 0, 9],
         [0, 0, 5, 0, 1, 0, 3, 0, 0]])
    test_board(board)
    test_board(Board(SudokuBoard().sudoku_maker()))
