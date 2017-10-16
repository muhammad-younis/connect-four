import sys
from final_board import *
from final_players import *
import random

class Connect4:
    '''Instances of this class simulate an interactive Connect-4 game.'''

    def __init__(self, opponent, toMove):
        '''
        Initializes the game.

        Arguments:
          opponent -- the computer opponent object
          toMove   -- the first player to move.  1 = human, 2 = computer.
        '''
        assert toMove in [1, 2]
        self.toMove = toMove
        self.opponent = opponent
        self.board = Connect4Board()
        self.nrows = self.board.getRows()
        self.ncols = self.board.getCols()
        self.moves = []

    def show(self):
        '''Print the board to the terminal, along with the player to move.'''

        print
        print '     top'
        print '-------------'
        for row in range(self.nrows-1, -1, -1):
            for col in range(0, self.ncols):
                val = self.board.get(row, col)
                if val == 0:
                    print '.',
                else:
                    print val,
            print
        print '-------------'
        print '0 1 2 3 4 5 6'
        print '   column'
        print

    def makeMove(self, col, player):
        '''
        Make a move on the board.

        Arguments:
          col    -- a valid column index
          player -- either 1 or 2
        '''

        if col < 0 or col >= self.ncols:
            raise MoveError('invalid move: %d' % col)
        self.board.makeMove(col, player)
        self.moves.append((player, col))

    def unmakeMove(self):
        '''
        Unmake a move on the board.  This means that the last move by
        both players is undone i.e. those locations on the board are cleared.

        Raise a MoveError exception if there are not enough moves to undo.
        '''

        if len(self.moves) > 1:
            self.board.unmakeMove(self.moves.pop()[1])
            self.board.unmakeMove(self.moves.pop()[1])
        else:
            raise MoveError('Not enough moves to undo!')

    def changePlayerToMove(self):
        '''Change the player to move.'''

        self.toMove = 3 - self.toMove   # changes 2 -> 1 and 1 -> 2

    def play(self):
        '''
        Play a game of Connect-4 interactively against the computer opponent.
        Stop if either player wins or if the board is full.  Allow the user to
        undo moves.
        '''

        game.show()
        print 'Player %d to move.\n' % self.toMove

        while True:
            try:
                if self.toMove == 1:  # player 1 = human
                    cmd = raw_input('*** Enter command: ')
                    cmd.strip()  # ignore whitespace
                    if cmd == 'q':
                        print 'Quitting...'
                        break
                    elif cmd == 'u':
                        print 'Undoing last move...'
                        self.unmakeMove()
                        self.show()
                        continue
                    else:  # assume it's a column number (a move)
                        sys.stdout.flush()
                        col = int(cmd)
                        self.makeMove(col, 1)
                        self.show()
                else:  # player 2 = computer
                    col = self.opponent.chooseMove(self.board.clone(), 2)
                    self.makeMove(col, 2)
                    print 'Computer plays on column %d...' % col
                    self.show()

                # Check for wins or draws.
                if self.board.isWin(col):
                    print "Game over: player %d wins!" % self.toMove
                    return

                if self.board.isDraw():
                    print "Game over: the game is a draw."
                    return

                self.changePlayerToMove()
                print 'Player %d to move.\n' % self.toMove

            except ValueError, e:
                print e
                print >> sys.stderr, 'Invalid command; try again...'

            except MoveError, e:
                print e
                print >> sys.stderr, 'Move error; try again...'

            except BoardError, e:
                print e
                print >> sys.stderr, 'Board error; try again...'

if __name__ == '__main__':
    players = ['random', 'simple', 'better', 'monty']

    print 'Computer players: %s' % players
    player = raw_input('Enter name of computer player: ')

    if player == 'random':
        opponent = RandomPlayer()
    elif player == 'simple':
        opponent = SimplePlayer()
    elif player == 'better':
        opponent = BetterPlayer()
    elif player == 'monty':
        nsims = int(raw_input('Enter number of simulations per move: '))
        assert nsims > 0
        player = SimplePlayer()
        opponent = Monty(nsims, player)
    else:
        print >> sys.stderr, 'Invalid player name.  Exiting.'
        sys.exit(1)

    toMove = random.choice([1, 2])

    print
    print 'First player to move: %d' % toMove
    print

    game = Connect4(opponent, toMove)
    game.play()

