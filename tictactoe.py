#!/usr/bin/env python3
"""A tic tac toe game."""


class IllegalMoveError(Exception):

    """Just a tic-tac-toe specific error."""

    def __init__(self):
        pass

    def __str__(self):
        pass


class Board():

    """A tic-tac-toe board and rules implementation"""

    def __init__(self, side_length=3):
        self.side_length = side_length
        self.state = [[0 for i in range(self.side_length)]
                      for j in range(self.side_length)]
        # The X's and O's are -1 and 1 for several reasons.
        # When keeping track of whose turn it is it allows us to simply
        # multiply the value by -1 to change turns.
        # It also allows to simply sum up rows and columns to determine
        # the winner.

        # for displaying the board
        self.translateDict = {1: 'O', -1: 'X', 0: '_'}

    def checkWinner(self):
        """Use elegant methods to check for a winner.
        Players' moves are stored internally 1 and -1, allowing
        lines to simply be summed to check for a winner."""
        transposed = transpose(self.state)
        # general solution using sums and transposed versions of the board
        states = [self.state, transposed, transpose(transposed[::-1])]
        # check each horiz and vert line
        for state in states:
            for line in state:
                if (abs(sum(line)) == self.side_length):
                    return self.translateToChar(line[0])

            # get sums of diagonals
            diagSums = [
                abs(sum([state[i][i] for i in range(self.side_length)])),
                abs(sum([state[self.side_length - i - 1][i]
                         for i in range(self.side_length)]))
            ]
            if self.side_length in diagSums:
                middle = self.side_length // 2 + self.side_length % 2 - 1
                return self.translateToChar(state[middle][middle])

        return None

    def makeMove(self, player, x, y):
        """Attempt a move and fail safely."""
        if self.state[y][x] not in [-1, 1]:
            try:
                self.state[y][x] = player
            except IndexError:
                raise IllegalMoveError
        else:
            raise IllegalMoveError

    def __str__(self):
        """Return string representation of the board."""
        out = "Board:\n" + '\n'.join(
            ['|' + '|'.join(
                [
                    self.translateToChar(col) for colnum, col in enumerate(row)
                ]
            ) + '|' + str(rowNum) for rowNum, row in enumerate(self.state)
            ]
        ) + '\n ' + " ".join([str(i) for i in range(self.side_length)])
        return out

    def translateToChar(self, c):
        return self.translateDict[c]


def transpose(l):
    """A standard matrix operation to re-slice the matrix"""
    return list(zip(*l))


def main():
    myboard = Board(3)
    print(myboard)
    player = -1
    winner = False
    while True:
        try:
            userMove = [
                int(i) for i in input(
                    "Enter move for {}.\nx y: ".format(
                        myboard.translateToChar(player)
                    )
                )
                .strip().split(' ')
            ]
            # there is only one type of valid input, a coordinate pair
            assert len(userMove) == 2
            myboard.makeMove(player, *userMove)
        except (AssertionError, ValueError):
            print("Invalid input!")
        except IllegalMoveError:
            print("ILLEGAL MOVE!")
        except KeyboardInterrupt:
            print("Quitting...")
            quit()
        else:
            winner = myboard.checkWinner()
            # simply flip the current player to pass the turn
            player *= -1
        # str is defined for Board, which makes this work
        print(myboard)
        # only check for a winner at the end
        if winner:
            print("The winner is {}!".format(winner))
            quit()

if __name__ == '__main__':
    main()
