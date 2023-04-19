import queue


class Square():
    def __init__(self,value = 0) -> None:
        self.domain = [1,2,3,4,5,6,7,8,9]
        self.constraints = []
        self.value = value
        if(self.value != 0):
            self.domain = [value]
    #def update(self)-> bool:
        #for node in self.constraints:
           # if(not node.domain.remove(self.value)):
             #   return False
        #return True
    def remove(self,value):
        contains = self.domain.__contains__(value)
        if(contains):
            self.domain.remove(value)
        if(len(self.domain) == 1):
            self.value = self.domain[0]
        return contains
    def setValue(self,value):
        self.value = value
    def getValue(self) -> int:
        return self.value
    def get_constraints(self):
        return self.constraints
    def add_constraints(self,constraints):
        self.constraints.extend(constraints)
    def constraint_update(self,constraint):
        if(self.value == 0):
            return False
        return constraint.remove(self.value)

#class Constraint():
    #def __init__(self) -> None:
        #pass

class Board():
    def __init__(self,init = None) -> None:
        self.board = []
        self.base = 3
        self.side = self.base**2
        if(init is None):
            self.initialize()
        else:
            self.initialize(init)
    def getRow(self,row,col):
        values = []
        for i in range(self.side):
            if(i != col):
                values.append(self.board[row][i])
        return values
    def getColumn(self,row,col):
        values = []
        for i in range(self.side):
            if(i != row):
                values.append(self.board[i][col])
        return values
    def getSquare(self,row,col):
        values = []
        box_row = row - (row % self.base)
        box_column = col - (col % self.base)
        for i in range(box_row, box_row + self.base):
            for j in range(box_column, box_column + self.base):
                if (i != row and j!= col):
                    values.append(self.board[row][col])
        return values
    
    def arc_inference(self):
        arc_queue = queue.Queue(maxsize=0)
        for i in range(self.side):
            for j in range(self.side):
                if(self.board[i][j].getValue() != 0):
                    arc_queue.put(self.board[i][j])

        while(not arc_queue.empty()):
            node = arc_queue.get()
            for constraint in node.get_constraints():
                if(node.constraint_update(constraint)):
                    arc_queue.put(constraint)
                    if(len(constraint.domain) == 0):
                        return False
            return True

    def initialize(self,init = None):
            for i in range(self.side):
                self.board.append([])
                for j in range(self.side):
                    if(init is None):
                        self.board[i].append(Square())
                    else:
                        self.board[i].append(Square(init[i][j]))
            for i in range(self.side):
                for j in range(self.side):
                    self.board[i][j].add_constraints(self.getColumn(i,j))
                    self.board[i][j].add_constraints(self.getRow(i,j))
                    self.board[i][j].add_constraints(self.getSquare(i,j))

    
    def __str__(self) -> str:
        string = ""
        for i in range(self.side):
            string = string + "\n"
            for j in range(self.side):
                string = string + str(self.board[i][j].getValue()) + " "
        return string

board = Board([[0,0,3,0,2,0,6,0,0],[9,0,0,3,0,5,0,0,1],[0,0,1,8,0,6,4,0,0],[0,0,8,1,0,2,9,0,0],[7,0,0,0,0,0,0,0,8],[0,0,6,7,0,8,2,0,0],[0,0,2,6,0,9,5,0,0],[9,0,0,2,0,3,0,0,9],[0,0,5,0,1,0,3,0,0]])
board.arc_inference()
print(board)
for i in range(board.side):
    for j in range(board.side):
        print(board.board[i][j].domain)
        


