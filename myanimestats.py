from menu import Menu
from animes import AnimesList
from edit import EditAnime
from new import NewAnime
from delete import DeleteAnime
from path import CheckPath, CheckProfile
from profile import CreateProfile

def main() -> int:
    choice: int = Menu()

    match choice[0]:
        case 0 | 1 | 2 | 3 | 4:
            anime = AnimesList(choice)
            if anime != '':
                if anime.startswith('<delete>'):
                    DeleteAnime(anime)
                else:
                    EditAnime(anime)
        case 5:
            NewAnime()
        case _:
            return 0

CheckPath()
if not CheckProfile():
    CreateProfile()

while True:
    return_id = main()
    if return_id == 0:
        break
