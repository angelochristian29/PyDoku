# import queue
import heapq
from dataclasses import dataclass, field
from typing import Any

from SudokuBoard import SudokuBoard
#from SudokuGUI import *
import pygame as pg

alphabet = "ABCDEFGHI"

class CSPGUIAdapter():
    def __init__(self,GUI,color,update) -> None:
        self.updateGUI = update
        self.GUI = GUI
        self.color = color
    def update(self,board,r,c,color):
        self.updateGUI(self.GUI,board,r,c,color)
                

class Integer():
    def __init__(self, value=0,square=None) -> None:
        self.value = value
        self.square= square

    def set(self, value):
        self.square.board.sum -= self.value
        self.value = value
        self.square.board.sum += self.value


    def get(self):
        return self.value


class Queue():
    def __init__(self) -> None:
        self.list = []

    def put(self, object):
        self.list.append(object)

    def get(self):
        return self.list.pop(0)

    def empty(self):
        return (len(self.list) == 0)

    def __str__(self) -> str:
        string = ""
        for item in self.list:
            string = string + str(item)
        return string


class Square():
    def __init__(self, name="", value=0,r=0,c=0,board=None) -> None:
        self.name = name
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.constraints = []
        self.value = Integer(value,self)
        self.coord = (r,c)
        if (self.value.get() != 0):
            self.domain = [value]
        self.degree = 0
        self.board = board

    def remove(self, value, removals=None):
        if removals is None:
            removals = []
        contains = self.domain.__contains__(value)
        if (contains):
            self.domain.remove(value)
            removals.append((self.domain, value))
            if (len(self.domain) == 1):
                self.value.set(self.domain[0])
                removals.append((self.value, 0))
                if (self.board.GUIAd is not None):
                    self.board.GUIAd.update(self.board,self.coord[0],self.coord[1],"red")
        return contains

    def setValue(self, value):
        self.value.set(value)

    def getValue(self) -> int:
        return self.value.get()

    def get_constraints(self):
        return self.constraints

    def add_constraints(self, constraints):
        self.constraints.extend(constraints)
        for constraint in constraints:
            if constraint.value.get() == 0:
                self.degree += 1

    def constraint_update(self, constraint, removals=None):
        if removals is None:
            removals = []
        if (self.value.get() == 0):
            return False
        return constraint.remove(self.value.get(),removals)

    def __str__(self) -> str:
        string = self.name + "\nValue: " + str(self.value.get()) + "\nDomain: "
        for value in self.domain:
            string = string + str(value) + " "
        return string

    def __eq__(self, __value: object) -> bool:
        return len(self.domain) == len(__value.domain)

    def __lt__(self, other):
        return len(self.domain) < len(other.domain)

    def __le__(self, other):
        return len(self.domain) <= len(other.domain)

    def __gt__(self, other):
        return len(self.domain) > len(other.domain)

    def __ge__(self, other):
        return len(self.domain) <= len(other.domain)

class Board():
    def __init__(self, init=None,GUIAd = None) -> None:
        self.board = []
        self.base = 3
        self.side = self.base ** 2
        self.GUIAd = GUIAd
        self.sum = 0
        self.initialize(init)

    def getRow(self, row, col):
        values = []
        for i in range(self.side):
            if (i != col):
                values.append(self.board[row][i])
        return values

    def getColumn(self, row, col):
        values = []
        for i in range(self.side):
            if (i != row):
                values.append(self.board[i][col])
        return values

    def getSquare(self, row, col):
        values = []
        box_row = row - (row % self.base)
        box_column = col - (col % self.base)
        for i in range(box_row, box_row + self.base):
            for j in range(box_column, box_column + self.base):
                if (i != row and j != col):
                    values.append(self.board[i][j])
        return values

    def arc_inference(self, arc_queue=None, removals=None):
        if removals is None:
            removals = []
        if (arc_queue is None):
            return False
        while (not arc_queue.empty()):
            node = arc_queue.get()
            for constraint in node.get_constraints():
                if (node.constraint_update(constraint,removals)):
                    arc_queue.put(constraint)
                    if (len(constraint.domain) == 0):
                        return False
        return True

    def initialize(self, init=None):
        for i in range(self.side):
            self.board.append([])
            for j in range(self.side):
                if (init is None):
                    self.board[i].append(Square(alphabet[i] + str(j + 1),0,i,j,board=self))
                else:
                    self.board[i].append(Square(alphabet[i] + str(j + 1), init[i][j],i,j,board=self))
                    self.sum += init[i][j]
        for i in range(self.side):
            for j in range(self.side):
                self.board[i][j].add_constraints(self.getColumn(i, j))
                self.board[i][j].add_constraints(self.getRow(i, j))
                self.board[i][j].add_constraints(self.getSquare(i, j))
        arc_queue = Queue()
        for i in range(self.side):
            for j in range(self.side):
                if (self.board[i][j].getValue() != 0):
                    arc_queue.put(self.board[i][j])
        self.arc_inference(arc_queue)

    def backtracking_search(self):
        heap = []
        for i in range(self.side):
            for j in range(self.side):
                if (self.board[i][j].getValue() == 0):
                    heapq.heappush(heap, self.board[i][j])
        return self.backtrack(heap)

    def backtrack(self, heap):
        if (len(heap) == 0  or self.sum == 405):
            return True
        square = heapq.heappop(heap)
        removals = []
        for value in square.domain:
            prev_value = square.value.get()
            square.value.set(value)
            if(self.GUIAd is not None):
                self.GUIAd.update(self,square.coord[0],square.coord[1],"blue")
            #print(square)
            #print(self)
            #print(self.sum)
            removals.append((square.value, prev_value))
            arc_queue = Queue()
            arc_queue.put(square)
            if (self.arc_inference(arc_queue, removals)):
                result = self.backtrack(heap) 
                if(result):
                    return result
            self.reverse_removals(removals)
        heapq.heappush(heap, square)  
        return False

    def reverse_removals(self, removals):
        for removed in removals:
            if (type(removed[0]) is Integer):
                removed[0].set(removed[1])
            else:
                list = removed[0]
                list.append(removed[1])
                list.sort()
        removals.clear()

    def __str__(self) -> str:
        string = "\n"
        for i in range(self.side):
            string = string + "\n"
            for j in range(self.side):
                string = string + str(self.board[i][j].getValue()) + " "
        return string

def test_board(test_board):
    print("Before\n" + str(test_board))
    test_board.arc_inference()
    print(test_board.backtracking_search())
    print("After\n" + str(test_board))

def debug_board(test_board):
    for i in range(test_board.side):
            for j in range(test_board.side):
                print(test_board.board[i][j])

board = Board([
[0, 3, 4, 0, 7, 0, 0, 0, 0],
[5, 9, 2, 0, 0, 4, 0, 0, 0],
[0, 8, 0, 0, 0, 0, 0, 0, 0],
[8, 0, 0, 0, 0, 0, 0, 2, 0],
[0, 0, 0, 0, 0, 0, 7, 0, 0],
[0, 1, 0, 0, 0, 0, 6, 0, 8],
[0, 6, 0, 7, 0, 0, 0, 5, 0],
[0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 5, 3, 6, 0, 0, 0, 0, 0]])
test_board(board)

board = Board()
test_board(board)

board = Board(
        [[0, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0],
         [0, 0, 8, 1, 0, 2, 9, 0, 0],
         [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0], [0, 0, 2, 6, 0, 9, 5, 0, 0],
         [8, 0, 0, 2, 0, 3, 0, 0, 9],
         [0, 0, 5, 0, 1, 0, 3, 0, 0]])
test_board(board)
random_board = Board(SudokuBoard().sudoku_maker())
test_board(random_board)
