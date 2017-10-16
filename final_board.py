
'''
final_board.py

This module contains classes that implement the Connect-4 board object.
'''

import copy

class MoveError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    an invalid move is made.
    '''
    pass

class BoardError(Exception):
    '''
    Instances of this class are exceptions which are raised when
    some erroneous condition relating to a Connect-Four board occurs.
    '''
    pass

class Connect4Board:
    '''
    Instance of this class manage a Connect-Four board, but do not
    manage the play of the game itself.
    '''

    def __init__(self):
        '''
        Initialize the board.
        '''

        self.board = []
        for i in range(6):
            self.board.append([0] * 7)
        self.rows = 6
        self.cols = 7


    def getRows(self):
        '''
        Return the number of rows.
        '''

        return self.rows

    def getCols(self):
        '''
        Return the number of columns.
        '''

        return self.cols

    def get(self, row, col):
        '''
        Arguments:
          row -- a valid row index
          col -- a valid column index

        Return value: the board value at (row, col).

        Raise a BoardError exception if the 'row' or 'col' value is invalid.
        '''

        if row < 0 or row > 5:
            raise BoardError ('Must select a row that exists!')
        if col > 6 or col < 0:
            raise BoardError ('Must select a col that exists!')
        return self.board[row][col]
            

    def clone(self):
        '''
        Return a clone of this board i.e. a new instance of this class
        such that changing the fields of the new instance will not
        affect the old instance.

        Return value: the new Connect4Board instance.
        '''
        
        copyboard = copy.deepcopy(self)

        return copyboard

    def possibleMoves(self):
        '''
        Compute the list of possible moves (i.e. a list of column numbers 
        corresponding to the columns which are not completely filled up).

        Return value: the list of possible moves
        '''

        possiblemoves= []
        for i, item in enumerate(self.board[5]):
            if item == 0:
                possiblemoves.append(i)
        return possiblemoves
            

    def makeMove(self, col, player):
        '''
        Make a move on the specified column for the specified player.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: none

        Raise a MoveError exception if a move cannot be made because the column
        is filled up, or if the column index or player number is invalid.
        '''

        if player > 2 or player < 1:
            raise MoveError ('Must select valid player (1 or 2)!')
        if col > 6 or col < 0:
            raise MoveError ('Must pick a col that exists!')
        if self.board[5][col] == 1 or self.board[5][col] == 2:
            raise MoveError ('Column is already full!')
        for i in range(6):
            if self.board[i][col] == 0:
                self.board[i][col] = player
                break
        
            

    def unmakeMove(self, col):
        '''
        Unmake the last move made on the specified column.

        Arguments:
          col -- a valid column index

        Return value: none

        Raise a MoveError exception if there is no move to unmake, or if the
        column index is invalid.
        '''

        if col > 6 or col < 0:
            raise MoveError ('Must pick a col that exists!')        
        if self.board[0][col] == 0:
            raise MoveError ('This column is empty!')
        for i in range(6):
            if self.board[5 - i][col] == 1 or self.board[5 - i][col] == 2:
                self.board[5 - i][col] = 0
                return
            

    def lastmoveincol(self, col):
        '''
        This is a helper function for the isWin method, it goes into a column
        and returns the row index and value of the last move in the form of a 
        tuple. Raises BoardError is the col selected to check for the last move
        is empty.
        '''
        if self.board[0][col] == 0:
            raise BoardError('This col is empty!')
        for i in range(6):
            if self.board[5 - i][col] == 1 or self.board[5 - i][col] == 2:  
                lastmove = [5 - i, self.board[5 - i][col]]
                return lastmove
        
    def verticalwintest(self, row, col, player):
        '''
        Checks if the last move made will result in a win from the vertical
        column
        
        Arguments: none
        
        Returns: True if vertical win, False if no vertical win
        
        
        '''

        if row - 3 < 0:
            return False
        else:
            if self.board[row - 1][col] == player and \
               self.board[row - 2][col] == player and \
               self.board[row - 3][col] == player:
                return True
            else: 
                return False
            
    def horizontalwintest(self, row, col, player):
        '''
        Checks if the last move made will result in a win from the horizontal
        row
        
        Arguments: none
        
        Returns: True if horizontal win, False if no horizontal win
        
        
        '''
        locations = []
        if self.board[row].count(player) >= 4:
            for (i, item) in enumerate(self.board[row]):
                if item == player:
                    locations.append(i)
            for i in locations:
                if i <= 3:
                    if self.board[row][i + 1] == player and \
                       self.board[row][i + 2] == player\
                       and self.board[row][i + 3] == player:
                        return True
            return False
        else:
            return False
        
    def diaganolwintest(self, row, col, player):
        '''
        This test essentially takes a point and locates the range of points
        that exist to the upperleft, upperright, lowerleft and lowerright of
        the point to test if 4 in a row was made in a diagonal direction.
        
        Returns true if diaganol win, returns false if no diaganol win.
        
        '''
        leftdiaganolpoints = []
        rightdiaganolpoints = []
        rightlocations = []
        leftlocations = []
        upperlimit = 5 - row
        lowerlimit = row 
        leftlimit =  col
        rightlimit = 6 - col
        topleftcol = col - min(upperlimit, leftlimit)
        topleftrow = row + min(upperlimit, leftlimit)
        botleftcol = col - min(lowerlimit, leftlimit)
        botleftrow = row - min(lowerlimit, leftlimit)
        for i in range(\
            min(upperlimit, leftlimit) + min(lowerlimit, rightlimit) + 1):
            leftdiaganolpoints.append(\
                self.board[topleftrow - i][topleftcol + i])
        for i in range(\
            min(lowerlimit, leftlimit) + min(upperlimit, rightlimit) + 1):
            rightdiaganolpoints.append(\
                self.board[botleftrow + i][botleftcol + i])
        if rightdiaganolpoints.count(player) >= 4:  
            for i, item in enumerate(rightdiaganolpoints):
                if item == player:
                    rightlocations.append(i) 
            for i in rightlocations:
                if i + 3 <= (len(rightdiaganolpoints) - 1):
                    if rightdiaganolpoints[i + 1] == player and \
                       rightdiaganolpoints[i + 2] == player\
                       and rightdiaganolpoints[i + 3] == player:
                        return True     
        if leftdiaganolpoints.count(player) >= 4:  
            for i, item in enumerate(leftdiaganolpoints):
                if item == player:
                    leftlocations.append(i) 
            for i in leftlocations:
                if i + 3 <= (len(leftdiaganolpoints) - 1):
                    if leftdiaganolpoints[i + 1] == player and \
                       leftdiaganolpoints[i + 2] == player\
                       and leftdiaganolpoints[i + 3] == player:
                        return True                    
        return False
                
    def isWin(self, col):
        '''
        Check to see if the last move played in column 'col' resulted in a win
        (four or more discs of the same color in a row in any direction).

        Argument: 
          col    -- a valid column index

        Return value: True if there is a win, else False

        Raise a BoardError exception if the column is empty (i.e. no move has
        ever been made in the column), or if the column index is invalid.
        '''
        if col > 6 or col < 0:
            raise BoardError ('Must pick a col that exists!')
        if self.board[0][col] == 0:
            raise BoardError ('Col is empty!')
        lastmove = self.lastmoveincol(col)
        player = lastmove[1]
        row = lastmove[0]

        if self.verticalwintest(row, col, player) == True:
            return True
        if self.horizontalwintest(row, col, player) == True:
            return True
        if self.diaganolwintest(row, col, player) == True:
            return True
        else:
            return False
        

    def isDraw(self):
        '''
        Check to see if the board is a draw because there are no more
        columns to play in.

        Precondition: This assumes that there is no win on the board.

        Return value: True if there is a draw, else False
        '''

        return (0 not in self.board[5])

    def isWinningMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a win.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a win, else False.

        Precondition: This assumes that the move can be made.
        '''

        testboard = self.clone()
        testboard.makeMove(col, player)
        return testboard.isWin(col)

    def isDrawingMove(self, col, player):
        '''
        Check to see if making the move 'col' by the player 'player'
        would result in a draw.  The board state does not change.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2

        Return value: True if the move would result in a draw, else False.

        Precondition: This assumes that the move can be made, and that the
        move has been checked to see that it does not result in a win.
        '''

        testboard = self.clone()
        testboard.makeMove(col, player)
        return testboard.isDraw()
        

