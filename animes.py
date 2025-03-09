import curses
import path

def DefineAnimesList(std, choice) -> str:
    category: char
    anime: str

    std.clear()
    std.refresh()

    win_out = curses.newwin(curses.LINES - 2, curses.COLS - 2, 1, 1)
    win_out.attrset(curses.color_pair(1))
    win_out.box()
    win_out.refresh()

    win = curses.newwin(curses.LINES - 4, curses.COLS - 6, 2, 3)
    win.attrset(curses.color_pair(1))
    win.box()
    win.refresh()

    match choice[0]:
        case 0:
            anime = Animes(std, choice, 'w', win)
        case 1:
            anime = Animes(std, choice, 'c', win)
        case 2:
            anime = Animes(std, choice, 'h', win)
        case 3:
            anime = Animes(std, choice, 'd', win)
        case 4:
            anime = Animes(std, choice, 'p', win)

    return anime

def AnimesList(choice) -> None:
    return curses.wrapper(DefineAnimesList, choice)

def Animes(std, choice, cat, win) -> str:
    file = open(path.animes, 'r')
    selected: int = 0
    animes: list = []
    anime_to_return: str

    win.addstr(2, 3, choice[1].capitalize(), curses.color_pair(1))
    for i in range(curses.COLS - 12):
        win.addstr(3, i + 3, '-', curses.A_NORMAL)

    for anime in file:
        if not anime.split('|')[1] == cat:
            continue
        animes.append(anime)

        Choices(cat, selected, animes, win)
    
    for i in range(curses.COLS - 12):
        win.addstr(curses.LINES - 8, i + 3, '-', curses.A_NORMAL)

    win.addstr(curses.LINES - 7, 5, 'q: back        d: delete        enter: edit', curses.A_NORMAL)
    win.refresh()

    while True:
        key = std.getch()
        match key:
            case curses.KEY_DOWN:
                selected += 1
                if selected > len(animes) - 1:
                    selected = 0
                Choices(cat, selected, animes, win)
                win.refresh()
            case curses.KEY_UP:
                selected -= 1
                if selected < 0:
                    selected = len(animes) -1
                Choices(cat, selected, animes, win)
                win.refresh()
            case 113: # q 
                anime_to_return = ''
                break
            case 100: # d
                anime_to_return = '<delete>' + animes[selected]
                break
            case 10: # enter
                anime_to_return =  animes[selected]
                break
    return anime_to_return
     
def Choices(cat, selected, animes, win) -> None:
    for i, anime in enumerate(animes):
        anime: str = anime.rstrip()
        name: str = anime.split('|')[0]
        category: str = anime.split('|')[1]
        total_seasons: str = anime.split('|')[2]
        current_season: str = anime.split('|')[3]
        total_eps: str = anime.split('|')[4]
        last_ep: str = anime.split('|')[5]
        rating: str = anime.split('|')[6]

        match cat:
            case 'w' | 'd' | 'h':
                anime = ' ' + name + ': season ' + current_season + '/' + total_seasons
                anime += ' ep ' + last_ep + '/' + total_eps + ' rating ' + rating + '*'
            case 'c':
                anime = ' ' + name + ': seasons ' + total_seasons + ' rating ' + rating + '*'
            case 'p':
                anime = ' ' + name + ': seasons ' + total_seasons

        if i == selected:
            args = curses.color_pair(2) | curses.A_STANDOUT | curses.A_BOLD
        else:
            args = curses.A_NORMAL
        for j in range(curses.COLS - len(anime) - 12):
            anime += ' '
        win.addstr(i + 4, 3, anime, args)
