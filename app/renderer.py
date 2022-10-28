import keyboard

from app.game import Game, Status, Turn
from utils.format import Format
from utils.palette import Palette


class Renderer(Format):
    game: Game
    cursor = [0, 0]
    log = ""

    def __init__(self, game) -> None:
        self.game = game

    def run(self) -> str:
        keyboard.add_hotkey("up", self.__up)
        keyboard.add_hotkey("down", self.__down)
        keyboard.add_hotkey("left", self.__left)
        keyboard.add_hotkey("right", self.__right)
        keyboard.add_hotkey("space", self.__exec)

        print(
            self.colorize(
                "\n(Use arrows to navigate, SPACE to place, q to exit)",
                Palette.GRAYED,
            )
        )
        print("\n\n\n")

        self.__render()
        while keyboard.read_key() != "q" and self.game.get_status() == Status.OK:
            pass
        keyboard.unhook_all()
        if self.game.get_status() == Status.GAME_OVER:
            return self.colorize(
                f"{self.game.get_turn().name} wins!",
                Palette.X if self.game.get_turn() == Turn.X else Palette.O,
            )
        elif self.game.get_status() == Status.DRAW:
            return self.colorize(
                "Draw",
                Palette.DEFAULT,
            )
        else:
            return self.colorize("Interrupted by user", Palette.ERROR)

    def place(self):
        self.game.make_turn(self.cursor[0], self.cursor[1])

    def __render(self):
        board = self.game.get_board()
        turn = self.game.get_turn()
        self.log += turn.name

        board_str = "\r\n".join(
            "".join(
                [
                    self.colorize(
                        f"[{self.colorize(board[row][col].name if board[row][col] else ' ', Palette.X if board[row][col] == Turn.X else Palette.O)}]",
                        Palette.DEFAULT,
                    )
                    if self.cursor != [row, col]
                    else self.colorize(
                        f"[{self.colorize(turn.name, Palette.HOVER_X if turn == Turn.X else Palette.HOVER_O)}]",
                        Palette.DEFAULT,
                    )
                    for col in range(self.game.SIZE)
                ]
            )
            for row in range(self.game.SIZE)
        )
        print("\r\033[A" * 4, end="")
        print(
            f"Turn: {self.colorize(turn.name, Palette.X if turn == Turn.X else Palette.O, True)}"
        )
        print(board_str)

    def __up(self):
        if self.cursor[0] > 0:
            self.cursor[0] -= 1
            self.__render()

    def __down(self):
        if self.cursor[0] < self.game.SIZE - 1:
            self.cursor[0] += 1
            self.__render()

    def __left(self):
        if self.cursor[1] > 0:
            self.cursor[1] -= 1
            self.__render()

    def __right(self):
        if self.cursor[1] < self.game.SIZE - 1:
            self.cursor[1] += 1
            self.__render()

    def __exec(self):
        self.place()
        self.__render()
