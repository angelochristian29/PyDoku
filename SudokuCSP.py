# coding: utf-8
# NAME: SudokuCSP.py
"""
Python module that defines classes used for CSP backtracking. Implements arc inferencing and CSP backtracking. 
"""
"""
AUTHOR: Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin


   Unpublished-rights reserved under the copyright laws of the United States.

   This data and information is proprietary to, and a valuable trade secret
   of, Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin. It is given 
   in confidence by Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin. 
   Its use, duplication, or disclosure is subject to
   the restrictions set forth in the License Agreement under which it has been
   distributed.

      Unpublished Copyright © 2022  Christian Hernandez, Felix Ohlgart, Angela Yang and Shivam Amin
      All Rights Reserved
"""
"""
Imports
"""
import heapq

alphabet = "ABCDEFGHI" #String used for the name of the variables ie. A1, A2

# Class used to adapt the previously created GUI class to CSP classes
class CSPGUIAdapter():
    def __init__(self,GUI,color,update) -> None:
        self.updateGUI = update
        self.GUI = GUI
        self.color = color
    def update(self,board,r,c,color): #Called when a value is changed in backtracking or arc inferencing
        self.updateGUI(self.GUI,board,r,c,color)
                
#Class defined to represent an integer. Needed to revert values after failure. Primitive type integer does not allow for this. 
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

#Defines a queue where the first object in is the first one out
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

#Defines a class representing each node/square on a Sudoku board. For CSP, it represents a variable, which contains a domain and constraints. 
class Square():
    def __init__(self, name="", value=0,r=0,c=0,board=None) -> None:
        self.name = name
        self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9] #Used for CSP, defines all possible values
        self.constraints = [] #Used for CSP, defines all constraints on the variable. For Sudoku, it is always an all-dif constraint. 
        self.value = Integer(value,self)
        self.coord = (r,c)
        if (self.value.get() != 0):
            self.domain = [value]
        self.degree = 0
        self.board = board
#Method to reduce domain based on given value. If the value exists in the domain, it is removed. 
#If the domain is reduced to 1 number, the value of the square is set to that value.
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

#Updates connected constraints based on the varaible's current value. Essentially an arc inference. 
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

#Represents the entire SudokuBoard, a 2d array of varaibles/nodes. Includes the CSP backtracking and arc inferencing algorithms.
class Board():
    def __init__(self, init=None,GUIAd = None) -> None:
        self.board = []
        self.base = 3
        self.side = self.base ** 2
        self.GUIAd = GUIAd
        self.sum = 0
        self.initialize(init) 

# Gets all the variables/nodes in a row. Used to define constraints.
    def getRow(self, row, col):
        values = []
        for i in range(self.side):
            if (i != col):
                values.append(self.board[row][i])
        return values
# Gets all the variables/nodes in a column. Used to define constraints.
    def getColumn(self, row, col):
        values = []
        for i in range(self.side):
            if (i != row):
                values.append(self.board[i][col])
        return values
# Gets all the variables/nodes in a square. Used to define constraints.
    def getSquare(self, row, col):
        values = []
        box_row = row - (row % self.base)
        box_column = col - (col % self.base)
        for i in range(box_row, box_row + self.base):
            for j in range(box_column, box_column + self.base):
                if (i != row and j != col):
                    values.append(self.board[i][j])
        return values
#Keeps track of variables with a queue. While the queue isn't empty, pops a variable/node, reduces the domain of its constraints by its value,
#and if the constraint receives a value from domain reduction, add it to the queue. Also checks for failure if domain size is reduced to 0. 
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
#Defines the board of variables. If a 2d array of numbers is given, sets variable values to those numbers, otherwise everything is set to 0.
# Also, does an initial domain reduction using arc inferencing. 
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

#Puts all values without a value onto a min heap. Calls backtrack() which does the actual search. 
    def backtracking_search(self):
        heap = []
        for i in range(self.side):
            for j in range(self.side):
                if (self.board[i][j].getValue() == 0):
                    heapq.heappush(heap, self.board[i][j])
        return self.backtrack(heap)
#The CSP backtracking algorithm. Implements minimum-remaining-values heuristic using the heap and forward checking using arc_inferencing()
#Chooses a number from a variable/nodes domain and sets its value to that number. Does arc_inferencing and if it succeeds, goes to the next square.
#If it doesnt, it reverts all of the changes.
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
            if (self.arc_inference(arc_queue, removals)): #Forward checking
                result = self.backtrack(heap) 
                if(result):
                    return result
            self.reverse_removals(removals) #Reverts changes
        heapq.heappush(heap, square)  
        return False
#Reverts the changes caused by forward checking and backtracking value assignments.
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
"""
Module execute/load check. REQUIRED
"""
if __name__ == '__main__':
    print("SudokuCSP.py: Module is executed.")
else:
    print("SudokuCSP.py: Module is imported.")