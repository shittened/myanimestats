import curses
import time

def DefineMenu(std) -> list:
    ascii: list = [
        '⣇⣿⠘⣿⣿⣿⡿⡿⣟⣟⢟⢟⢝⠵⡝⣿⡿⢂⣼⣿⣷⣌⠩⡫⡻⣝⠹⢿⣿⣷',
        '⡆⣿⣆⠱⣝⡵⣝⢅⠙⣿⢕⢕⢕⢕⢝⣥⢒⠅⣿⣿⣿⡿⣳⣌⠪⡪⣡⢑⢝⣇',
        '⡆⣿⣿⣦⠹⣳⣳⣕⢅⠈⢗⢕⢕⢕⢕⢕⢈⢆⠟⠋⠉⠁⠉⠉⠁⠈⠼⢐⢕⢽',
        '⡗⢰⣶⣶⣦⣝⢝⢕⢕⠅⡆⢕⢕⢕⢕⢕⣴⠏⣠⡶⠛⡉⡉⡛⢶⣦⡀⠐⣕⢕',
        '⡝⡄⢻⢟⣿⣿⣷⣕⣕⣅⣿⣔⣕⣵⣵⣿⣿⢠⣿⢠⣮⡈⣌⠨⠅⠹⣷⡀⢱⢕',
        '⡝⡵⠟⠈⢀⣀⣀⡀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⢈⡋⠴⢿⡟⣡⡇⣿⡇⡀⢕',
        '⡝⠁⣠⣾⠟⡉⡉⡉⠻⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣦⣥⣿⡇⡿⣰⢗⢄',
        '⠁⢰⣿⡏⣴⣌⠈⣌⠡⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣉⣉⣁⣄⢖⢕⢕⢕',
        '⡀⢻⣿⡇⢙⠁⠴⢿⡟⣡⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣵⣵⣿',
        '⡻⣄⣻⣿⣌⠘⢿⣷⣥⣿⠇⣿⣿⣿⣿⣿⣿⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿',
        '⣷⢄⠻⣿⣟⠿⠦⠍⠉⣡⣾⣿⣿⣿⣿⣿⣿⢸⣿⣦⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟',
        '⡕⡑⣑⣈⣻⢗⢟⢞⢝⣻⣿⣿⣿⣿⣿⣿⣿⠸⣿⠿⠃⣿⣿⣿⣿⣿⣿⡿⠁⣠',
        '⡝⡵⡈⢟⢕⢕⢕⢕⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⠿⠋⣀⣈⠙',
        '⡝⡵⡕⡀⠑⠳⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢉⡠⡲⡫⡪⡪⡣',
    ]
    choices: list = [
        'currently watching anime',
        'completed anime',
        'anime on hold',
        'dropped anime',
        'plan to watch anime',
        'new anime',
        'stats',
        'options',
        'quit'
    ]
    selected: int = 0

    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.curs_set(False)
    std.clear()
    std.refresh()

    topwin_out = curses.newwin(17, 35, 6, curses.COLS // 2 - 18) #HWYX
    topwin_out.attrset(curses.color_pair(1))
    topwin_out.box()
    topwin_out.refresh()
    
    topwin = curses.newwin(15, 31, 7, curses.COLS // 2 - 16) #HWYX
    for i, line in enumerate(ascii):
        topwin.addstr(i, 0, line, curses.A_NORMAL)
    topwin.attrset(curses.color_pair(1))
    topwin.box()
    topwin.refresh()

    botwin_out = curses.newwin(21, 35, 23, curses.COLS // 2 - 18)
    botwin_out.attrset(curses.color_pair(1))
    botwin_out.box()
    botwin_out.refresh()
    
    botwin = curses.newwin(19, 31, 24, curses.COLS // 2 - 16)
    botwin.addstr(2, 3, 'Ohayo onii-chan!!', curses.color_pair(1))
    botwin.addstr(3, 3, 'Would you like to:', curses.color_pair(1))
    botwin.addstr(4, 2, '---------------------------')

    Choices(choices, selected, botwin)

    botwin.addstr(14, 2, '---------------------------')
    botwin.addstr(15, 3, 'Or perhaps u\'d like to', curses.color_pair(1))
    botwin.addstr(16, 3, 'do me instead?', curses.color_pair(1))
    botwin.attrset(curses.color_pair(1))
    botwin.box()
    botwin.refresh()

    while True:
        time.sleep(0.01)
        key = std.getch()
        match key:
            case curses.KEY_DOWN:
                selected += 1
                if selected > len(choices) - 1:
                    selected = 0
                Choices(choices, selected, botwin)
                botwin.refresh()
            case curses.KEY_UP:
                selected -= 1
                if selected < 0:
                    selected = len(choices) - 1
                Choices(choices, selected, botwin)
                botwin.refresh()
            case 10: # enter
                return [selected, choices[selected]]
def Menu() -> None:
    return curses.wrapper(DefineMenu)

def Choices(choices, selected, win) -> None:
    for i, choice in enumerate(choices):
        choice = ' ' + choice
        for j in range(31 - 2 - len(choice) - 3):
            choice += ' '
        if i == selected:
            args = curses.color_pair(2) | curses.A_BOLD | curses.A_STANDOUT
        else:
            args = curses.A_NORMAL
        win.addstr(i + 5, 2, choice, args)

