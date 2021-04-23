from flask import Flask
from flask import request
import json
from steamTest import findAppId, findName
import urllib.request


app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello There! Work in progress :)</h1>"

@app.route('/steam/players/pajbot/<string:gameName>')
def playersText(gameName):
    numberSeparator = ',' # '\xa0' twitch seems to remove non breaking spaces Sadge
    game = json.loads(findAppId(gameName))
    steamApiUrl = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid="
    try:
        response = urllib.request.urlopen(steamApiUrl + str(game["appid"]))
    except Exception as ex:
        return str(ex)
    playersOnline = json.loads(response.read())["response"]["player_count"]
    return "The game {} currently has {} players online. https://steamcharts.com/app/{}/".format(game["name"], f"{playersOnline:,}".replace(',', numberSeparator), game["appid"])

@app.route('/steam/players/<int:appid>')
def playersOnline(appid):
    steamApiUrl = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid="
    try:
        response = urllib.request.urlopen(steamApiUrl + str(appid))
    except Exception as ex:
        return str(ex)
    paramText = request.args.get('text', default = 'false', type = str)
    if response.getcode() != 200:
        return "Error getting online player count, code : {}".format(response.getcode())
    else:
        playersOnline = json.loads(response.read())["response"]["player_count"]
        if paramText == "true":
            return "The game {} currently has {} players online.".format(findName(appid), playersOnline)
        else:
            return str(playersOnline)

@app.route('/steam/id/<string:gameName>')
def steamIdOnly(gameName):
    return str(json.loads(findAppId(gameName))["appid"])

@app.route('/steam/<string:gameName>')
def steam(gameName):
    if gameName == "":
        return "0"
    else:
        jsonResponse = findAppId(gameName)
        paramText = request.args.get('text', default = 'false', type = str)
        if paramText == "true":
            decoded = json.loads(jsonResponse)
            return "Found the game {0} with the appid {1} (match confidence {2}%), https://store.steampowered.com/app/{1}/".format(decoded["name"], decoded["appid"], decoded["matchscore"])
        else:
            return jsonResponse

if __name__ == "__main__":
    app.run(host='0.0.0.0')
