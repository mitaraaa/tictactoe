import enum


class Status(enum.Enum):
    OK = 0
    GAME_OVER = 1
    DRAW = 2


class Turn(enum.Enum):
    X = 0
    O = 1


class Game:
    SIZE = 3
    board: list[list[Turn]]
    turn: Turn
    status: Status = Status.OK

    def __init__(self) -> None:
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        self.turn = Turn.X

    def __change_turn(self):
        if not self.__validate():
            self.status = Status.DRAW if self.__validate_draw() else Status.GAME_OVER
            return

        if self.__validate_draw():
            self.status = Status.DRAW
            return

        self.turn = Turn.O if self.turn == Turn.X else Turn.X

    def __validate_draw(self) -> bool:
        return [sum(square is None for square in row) for row in self.board].count(
            0
        ) == self.SIZE

    def __validate(self) -> bool:
        valid = True

        for turn in Turn:
            valid = valid and (
                [sum(col == turn for col in row) for row in self.board].count(3) == 0
                and [
                    sum(row[i] == turn for row in self.board) for i in range(self.SIZE)
                ].count(3)
                == 0
                and sum(self.board[row][row] == turn for row in range(self.SIZE)) != 3
                and sum(
                    self.board[row][self.SIZE - row - 1] == turn
                    for row in range(self.SIZE)
                )
                != 3
            )

        return valid

    def make_turn(self, row, col):
        if not self.board[row][col]:
            self.board[row][col] = self.turn
        else:
            return False

        self.__change_turn()
        return True

    def restart(self):
        self.__init__()

    def get_board(self) -> list[list[Turn]]:
        return self.board

    def get_turn(self) -> Turn:
        return self.turn

    def get_status(self) -> Status:
        return self.status
