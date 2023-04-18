class Square():
    def __init__(self) -> None:
        self.domain = [1,2,3,4,5,6,7,8,9]
        self.constraints = []
class Constraint():
    def __init__(self) -> None:
        pass
class Board():
    def __init__(self) -> None:
        self.board = [[]]
        self.base = 3
        self.side = self.base**2
    def getRow(self,row,col):
        values = []
        for i in range(self.side):
            if(i != col):
                values.add(self.board[row][i])
        return values
    def getColumn(self,row,col):
        values = []
        for i in range(self.side):
            if(i != col):
                values.add(self.board[i][col])
        return values
    def getSquare(self,row,col):
        values = []
        for i in range(row, row + self.base):
            for j in range(box_column, box_column + self.base):
                if board[i][j] == num:
                    return False



