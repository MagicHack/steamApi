import json
import sys
from fuzzywuzzy import fuzz
import pathlib
import time
import subprocess
import urllib.request

jsonGameFile = 'steam.json'
data = None

steamGameListUrl = "http://api.steampowered.com/ISteamApps/GetAppList/v0002/"


def get_last_file_update():
    file = pathlib.Path(jsonGameFile)
    if file.exists():
        return round(time.time() - file.stat().st_mtime)
    return -1


def read_game_file():
    global data
    with open(jsonGameFile) as f:
        data = json.load(f)
        f.close()


def update_steam_file():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(steamGameListUrl, "steam.json")


def check_update_game_data():
    update_frequency = 12 * 60 * 60  # How often to refresh the json in seconds
    file = pathlib.Path(jsonGameFile)
    if file.exists():
        time_since_last_update = time.time() - file.stat().st_mtime
        if time_since_last_update > update_frequency:
            print("Updating file, last update {} hours ago".format(time_since_last_update / 60 / 60))
            update_steam_file()
            read_game_file()
    else:
        print("json not found, fetching it")
        update_steam_file()
        read_game_file()


def find_name(appid):
    for app in data["applist"]["apps"]:
        if app["appid"] == appid:
            return app["name"]
    return "Error : game not found"


def find_app_id(name):
    check_update_game_data()
    read_game_file()
    best_match_name = ""
    best_match = -1
    best_ratio = 0
    for app in data["applist"]["apps"]:
        app_name = app["name"]
        search_name = name
        app_id = app["appid"]
        fuzz_ratio = fuzz.ratio(app_name.lower(), search_name.lower())
        if fuzz_ratio > best_ratio:
            best_ratio = fuzz_ratio
            best_match = app_id
            best_match_name = app_name
            if best_ratio == 100:
                break
    print("Found app {} with fuzz ratio of {}, id {}".format(best_match_name, best_ratio, best_match))
    response = {"appid": best_match, "name": best_match_name, "matchscore": best_ratio}
    return json.dumps(response)


# while True:
#   name = input("App name to search for: ")
#   findAppId(name)

check_update_game_data()
