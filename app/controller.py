import os
import enum
from app.game import Game

from utils.menu import Menu
from app.renderer import Renderer


class Stage(enum.Enum):
    MENU = 0
    GAME = 1
    RESTART_MENU = 2


class Controller:
    stage: Stage
    game: Game

    def __init__(self) -> None:
        self.stage = Stage.MENU

    def start(self):
        self.__update()

    def __update(self):
        match self.stage:
            case Stage.MENU:
                menu = Menu(["Start", "Exit"])

                menu.bind("Start", self.set_stage, Stage.GAME)
                menu.bind("Exit", self.exit)

                menu.render()
            case Stage.GAME:
                self.game = Game()
                renderer = Renderer(self.game)
                print(renderer.run())
                self.set_stage(Stage.RESTART_MENU)
            case Stage.RESTART_MENU:
                menu = Menu(["Try again", "Exit"], "Continue?")

                menu.bind("Try again", self.set_stage, Stage.GAME)
                menu.bind("Exit", self.exit)

                menu.render()

    def set_stage(self, stage: Stage):
        self.stage = stage
        self.__update()

    def exit(self):
        os._exit(0)
