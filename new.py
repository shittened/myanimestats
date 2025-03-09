import curses
import path

def DefineNewAnime(std) -> None:
    name: str
    status: str
    total_seasons: str
    current_season: str
    total_eps: str
    last_ep: str
    rating: str
    
    statuses: list = ['w', 'c', 'h', 'd', 'p']
    errors: list = []
    
    std.clear()
    std.refresh()

    win_out = curses.newwin(curses.LINES - 2, curses.COLS - 2, 1, 1)
    win_out.attrset(curses.color_pair(1))
    win_out.box()
    win_out.refresh()

    win = curses.newwin(curses.LINES - 4, curses.COLS - 6, 2, 3)
    win.box()

    win.addstr(2, 4, 'Add new anime', curses.color_pair(1) | curses.A_BOLD)
    win.addstr(3, 4, 'Don\'t use |')
    win.addstr(4, 4, 'Don\'t leave blank')

    win.addstr(6, 4, 'Edit name', curses.color_pair(1) | curses.A_BOLD)
    name = Input(win, 7, 4, curses.COLS - 9 - 6 - 2, False)
    if '|' in name:
        errors.append('Name: don\'t use |')
    if name == '':
        errors.append('Name: don\'t leave blank')
    if CheckDuplicate(name):
        errors.append('Name: Anime already in database')

    win.addstr(9, 4, 'Edit status', curses.color_pair(1) | curses.A_BOLD)
    status = Input(win, 10, 4, 1, True)
    if status == '':
        errors.append('Status: don\'t leave blank')
    if not status in statuses:
        errors.append('Status: choose from w(watching) / c(completed) / h(on hold) / d(dropped) / p(plan to watch)')

    win.addstr(12, 4, 'Edit number of seasons', curses.color_pair(1) | curses.A_BOLD)
    total_seasons = Input(win,13, 4, 3, False)
    if total_seasons == '':
        errors.append('Total seasons: don\'t leave blank')
    if not total_seasons.isdigit():
        errors.append('Total seasons: must be a number')

    match status:
        case 'w' | 'd' | 'h':
            win.addstr(15, 4, 'Edit current season', curses.color_pair(1) | curses.A_BOLD)
            current_season = Input(win, 16, 4, 3, False)
            if current_season == '':
                errors.append('Current season: don\'t leave blank')
            if not current_season.isdigit():
                errors.append('Current season: must be a number')

            win.addstr(18, 4, 'Edit total episodes of current season', curses.color_pair(1) | curses.A_BOLD)
            total_eps = Input(win, 19, 4, 5, False)
            if total_eps == '':
                errors.append('Total episodes: don\'t leave blank')
            if not total_eps.isdigit():
                errors.append('Total episodes: must be a number')

            win.addstr(21, 4, 'Edit last episode watched', curses.color_pair(1) | curses.A_BOLD)
            last_ep = Input(win, 22, 4, 5, False)
            if last_ep == '':
                errors.append('Last episode: don\'t leave blank')
            if not last_ep.isdigit():
                errors.append('Last episode: must be a number')
            
            win.addstr(24, 4, 'Edit rating', curses.color_pair(1) | curses.A_BOLD)
            rating = Input(win, 25, 4, 2, False)
            if rating == '':
                errors.append('Rating: don\'t leave blank')
            if not rating.isdigit():
                errors.append('Rating: must be a number')

        case 'c':
            win.addstr(15, 4, 'Edit rating', curses.color_pair(1) | curses.A_BOLD)
            rating = Input(win, 16, 4, 2, False)
            if rating == '':
                errors.append('Rating: don\'t leave blank')
            if not rating.isdigit():
                errors.append('Rating must: be a number')

    if len(errors) > 0:
        return ErrorScreen(std, win, errors)
    else:
        anime_raw = [name, status, total_seasons, current_season, total_eps, last_ep, rating]
        return SuccesScreen(std, win, anime_raw)

def NewAnime() -> None:
    return curses.wrapper(DefineNewAnime)

def Input(win, y, x, lenght, is_status):
    prompt_len: int

    if is_status:
        win.addstr(y, x, '[w/c/h/d/p] > ', curses.color_pair(1) | curses.A_BOLD)
        prompt_len = 14
    else:
        win.addstr(y, x, '> ', curses.color_pair(1) | curses.A_BOLD)
        prompt_len = 2
    curses.echo()
    curses.curs_set(1)
    input = win.getstr(y, x + prompt_len, lenght)
    curses.noecho()
    curses.curs_set(0)
    win.refresh()
    return input.decode('utf-8')

def SuccesScreen(std, win, anime_raw) -> None:
    win.clear()
    win.box() 
    Save(win, anime_raw)
    win.addstr(2, 4, 'Succes', curses.color_pair(1) | curses.A_BOLD)
    win.addstr(4, 4, anime_raw[0] + ' added')
    win.refresh()
    std.getch()

def ErrorScreen(std, win, errors) -> None:
    win.clear()
    win.box()
    win.addstr(2, 4, 'Error', curses.color_pair(1) | curses.A_BOLD)
    for i, error in enumerate(errors):
        win.addstr(i + 4, 4, error)
    win.refresh()
    std.getch()

def Save(win, anime_raw) -> None:
    anime: str = '|'.join(anime_raw)

    with open(path.animes, 'a') as file:
        file.write(anime)

def CheckDuplicate(name) -> bool:
    animes_db: str
    db_animes: list = []

    with open(path.animes) as file:
        animes_db = file.readlines()

    for line in animes_db:
        db_anime_name = line.split('|')[0].lower()
        db_animes.append(db_anime_name)

    if name.lower() in db_animes:
        return True
    else:
        return False
