import curses
import path

def DefineCreateProfile(std) -> None:
    std.clear()
    std.addstr(0, 0, 'create profile') # TODO
    std.refresh()
    std.getch()

def CreateProfile() -> None:
    return curses.wrapper(DefineCreateProfile)
