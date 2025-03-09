import curses
import path

def DefineDeleteAnime(std, anime) -> None:
    anime: str = anime.split('>')[1]
    name: str = anime.split('|')[0]
    choices: list = ['YES', 'NO', 'ROBLOX']
    selected: int = 1

    std.clear()
    std.refresh()

    win_out = curses.newwin(16, 60, 20, curses.COLS // 2 - 30) #HWYX
    win_out.attrset(curses.color_pair(1))
    win_out.box()
    win_out.refresh()

    win = curses.newwin(14, 56, 21, curses.COLS // 2 - 28) #HWYX
    win.box()
    if len(name) > 35:
        name = name[:35] + '...'
    win.addstr(2, 4, 'Delete ' + name + '?!', curses.color_pair(1) | curses.A_BOLD)
    Choices(choices, selected, win)

    while True:
        key = std.getch()
        match key:
            case curses.KEY_DOWN:
                selected += 1
                if selected > len(choices) - 1:
                    selected = 0
                Choices(choices, selected, win)
            case curses.KEY_UP:
                selected -= 1
                if selected < 0:
                    selected = len(choices) - 1
                Choices(choices, selected, win)
            case 10:
                match choices[selected]:
                    case 'YES':
                        Delete(anime, name, win, std)
                        break
                    case 'NO':
                        break
                    case _:
                        break

def DeleteAnime(anime) -> None:
    return curses.wrapper(DefineDeleteAnime, anime)

def Choices(choices, selected, win) -> None:
    for i, choice in enumerate(choices):
        choice = ' ' + choice
        for j in range(56 - 6 - len(choice) - 1):
            choice += ' '
        if i == selected:
            args = curses.color_pair(2) | curses.A_BOLD | curses.A_STANDOUT
        else:
            args = curses.A_NORMAL
        win.addstr(5 + i * 2, 4, choice, args)
        win.refresh()

def Delete(anime, name, win, std):
    animes_db: str

    with open(path.animes, 'r') as file:
        animes_db = file.readlines()

    for i, anime_in_db in enumerate(animes_db):
        if anime_in_db == anime:
            animes_db[i] = ''.rstrip()

    with open(path.animes, 'w') as file:
        file.writelines(animes_db)

    win.clear()
    win.addstr(2, 4, name + ' deleted')
    a.box()
    win.refresh()
    std.getch()
