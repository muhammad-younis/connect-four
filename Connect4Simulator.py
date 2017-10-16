'''
Connect4Simulator.py

This module contains classes to simulate a connect-4 game with two computer
players.
'''

import random

class Connect4Simulator:
    '''
    This simulates a Connect-4 game with two computer players starting from a 
    particular board state.
    '''

    def __init__(self, board, player1, player2, toMove):
        '''
        Initialize the simulator.  

        Arguments:
          board   -- the current board state (a Connect4Board)
          player1 -- the player who is player 1
          player2 -- the player who is player 2
          toMove  -- the next player to move (1 or 2)
        '''

        assert toMove in [1, 2]
        self.board   = board
        self.player1 = player1
        self.player2 = player2
        self.toMove  = toMove

    def simulate(self):
        '''
        Simulate the current game until completion.

        Return value: 
          0 means a draw
          1 means player 1 won
          2 means player 2 won
        '''

        if self.board.isDraw():  # in case there are no moves...
            return 0

        while True:
            if self.toMove == 1:
               move = self.player1.chooseMove(self.board, 1)
            else:
               move = self.player2.chooseMove(self.board, 2)

            self.board.makeMove(move, self.toMove)
            if self.board.isWin(move):
                return self.toMove
            elif self.board.isDraw():
                return 0
            else:
                self.toMove = 3 - self.toMove

