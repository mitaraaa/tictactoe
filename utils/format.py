class Format:
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

    def __init__(self) -> None:
        pass

    def __get_color(self, red, green, blue, background=False):
        return f"\033[{48 if background else 38};2;{red};{green};{blue}m"

    def colorize(self, text: str, rgb: tuple[int], background=False) -> str:
        (red, green, blue) = rgb
        return self.__get_color(red, green, blue, background) + text + self.RESET

    def underline(self, text: str):
        return self.UNDERLINE + text + self.RESET
