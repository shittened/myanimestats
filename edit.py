import curses
import path

def DefineEditAnime(std, anime) -> None:
    name: str = anime.split('|')[0]
    status: str = anime.split('|')[1]
    total_seasons: str = anime.split('|')[2]
    current_season: str = anime.split('|')[3]
    total_eps: str = anime.split('|')[4]
    last_ep: str = anime.split('|')[5]
    rating: str = anime.split('|')[6]
    old_anime: str = anime

    new_name: str
    new_status: str
    new_total_seasons: str
    new_current_season: str
    new_total_eps: str
    new_last_ep: str
    new_rating: str
    new_anime_raw: list = []

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

    win.addstr(2, 4, 'Editing ' + name, curses.color_pair(1) | curses.A_BOLD)
    win.addstr(3, 4, 'Leave blank for default')
    win.addstr(4, 4, 'Don\'t use |')

    win.addstr(6, 4, 'Edit name', curses.color_pair(1) | curses.A_BOLD)
    win.addstr(7, 4, 'Default: ' + name)
    new_name = Input(win, 8, 4, curses.COLS - 9 - 6 - 2, False)
    if '|' not in new_name:
        if new_name != '':
            if not CheckDuplicate(new_name):
                name = new_name
            else:
                errors.append('Name: Anime already in database')
    else:
        errors.append('Name: don\'t use |')

    win.addstr(10, 4, 'Edit status', curses.color_pair(1) | curses.A_BOLD)
    win.addstr(11, 4, 'Default: ' + status)
    new_status = Input(win, 12, 4, 1, True)
    if new_status != '':
        if new_status in statuses:
            status = new_status
        else:
            errors.append('Status: choose from w(watching) / c(completed) / h(on hold) / d(dropped) / p(plan to watch)')

    win.addstr(14, 4, 'Edit number of seasons', curses.color_pair(1) | curses.A_BOLD)
    win.addstr(15, 4, 'Default: ' + total_seasons)
    new_total_seasons = Input(win,16, 4, 3, False)
    if new_total_seasons != '':
        if new_total_seasons.isdigit():
            total_seasons = new_total_seasons
        else:
            errors.append('Total seasons: must be a number')

    match status:
        case 'w' | 'd' | 'h':
            win.addstr(18, 4, 'Edit current season', curses.color_pair(1) | curses.A_BOLD)
            win.addstr(19, 4, 'Default: ' + current_season)
            new_current_season = Input(win, 20, 4, 3, False)
            if new_current_season != '':
                if new_current_season.isdigit():
                    current_season = new_current_season
                else:
                    errors.append('Current season: must be a number')

            win.addstr(22, 4, 'Edit total episodes of current season', curses.color_pair(1) | curses.A_BOLD)
            win.addstr(23, 4, 'Default: ' + total_eps)
            new_total_eps = Input(win, 24, 4, 5, False)
            if new_total_eps != '':
                if new_total_eps.isdigit():
                    total_eps = new_total_eps
                else:
                    errors.append('Total episodes: must be a number')

            win.addstr(26, 4, 'Edit last episode watched', curses.color_pair(1) | curses.A_BOLD)
            win.addstr(27, 4, 'Default: ' + last_ep)
            new_last_ep = Input(win, 28, 4, 5, False)
            if new_last_ep != '':
                if new_last_ep.isdigit():
                    last_ep = new_last_ep
                else:
                    errors.append('Last episode: must be a number')
            
            win.addstr(30, 4, 'Edit rating', curses.color_pair(1) | curses.A_BOLD)
            win.addstr(31, 4, 'Default: ' + rating)
            new_rating = Input(win, 32, 4, 2, False)
            if new_rating != '':
                if new_rating.isdigit():
                    rating = new_rating
                else:
                    errors.append('Rating must: be a number')

        case 'c':
            win.addstr(18, 4, 'Edit rating', curses.color_pair(1) | curses.A_BOLD)
            win.addstr(19, 4, 'Default: ' + rating)
            new_rating = Input(win, 20, 4, 2, False)
            if new_rating != '':
                if new_rating.isdigit():
                    rating = new_rating
                else:
                    errors.append('Rating: must be a number')

    if len(errors) > 0:
        return ErrorScreen(std, win, errors)
    else:
        new_anime_raw = [name, status, total_seasons, current_season, total_eps, last_ep, rating]
        return SuccesScreen(std, win, old_anime, new_anime_raw)

def EditAnime(anime) -> None:
    return curses.wrapper(DefineEditAnime, anime)

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

def SuccesScreen(std, win, old_anime, new_anime_raw) -> None:
    win.clear()
    win.box() 
    Save(win, old_anime, new_anime_raw)
    win.addstr(2, 4, 'Succes', curses.color_pair(1) | curses.A_BOLD)
    win.addstr(4, 4, 'Changes saved')
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

def Save(win, old_anime, new_anime_raw) -> None:
    animes_db: str
    new_anime: str = '|'.join(new_anime_raw)

    with open(path.animes, 'r') as file:
        animes_db = file.readlines()

    for i, anime_in_db in enumerate(animes_db):
        if anime_in_db == old_anime:
            animes_db[i] = new_anime

    with open(path.animes, 'w') as file:
        file.writelines(animes_db)

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
