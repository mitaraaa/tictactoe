import keyboard
from typing import Callable

from utils.palette import Palette
from utils.format import Format


class Menu(Format):
    name: str = " TicTacToe "

    cursor: int = 0
    options: dict
    params: dict = {}

    def __init__(self, options: list[str], name=None) -> None:
        self.options = {option: "" for option in options}
        self.name = name or self.name

    def bind(self, option: str, bind: Callable, params=None) -> None:
        self.options[option] = bind

        if params:
            self.params[option] = params

    def render(self):
        keyboard.add_hotkey("up", self.__up)
        keyboard.add_hotkey("down", self.__down)

        print(self.colorize(self.name, (0, 0, 0), True))
        print(
            self.colorize("(Use arrows to navigate, SPACE to select)", Palette.GRAYED)
        )
        print("\n" * (len(self.options) - 2))
        self.__render()
        keyboard.wait("space")
        keyboard.unhook_all()
        self.__exec()

    def __render(self):
        menu = "\r\n".join(
            [
                self.colorize(
                    ("► " if index == self.cursor else "  ") + option,
                    Palette.SELECTED if index == self.cursor else Palette.DEFAULT,
                )
                for index, option in enumerate(self.options)
            ]
        )

        print("\r\033[A" * (len(self.options) - 1), end="")
        print(menu, end="")

    def __up(self):
        if self.cursor > 0:
            self.cursor -= 1
            self.__render()

    def __down(self):
        if self.cursor < len(self.options) - 1:
            self.cursor += 1
            self.__render()

    def __exec(self):
        if not callable(type(list(self.options.values())[self.cursor])):
            return

        if self.params.get(list(self.options.keys())[self.cursor]):
            list(self.options.values())[self.cursor](
                self.params.get(list(self.options.keys())[self.cursor])
            )
        else:
            list(self.options.values())[self.cursor]()
