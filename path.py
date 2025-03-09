import os

home: str = os.getenv('HOME')
save_path: str = home + '/.config/myanimestats'
profile: str = save_path + '/profile.txt'
animes: str = save_path + '/animes.txt'

def CheckPath() -> None:
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    if not os.path.isfile(profile):
        open(profile, 'w').close()
    if not os.path.isfile(animes):
        open(animes, 'w').close()
    return

def CheckProfile() -> bool:
    profile_content: str

    with open(profile, 'r') as file:
        profile_content = file.readlines()

    if len(profile_content) > 1:
        return True
    else:
        return False
