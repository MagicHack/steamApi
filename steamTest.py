import json
import sys
from fuzzywuzzy import fuzz
import pathlib
import time
import subprocess
import urllib.request

jsonGameFile = 'steam.json'
data = None

steamGameListUrl = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"

def getLastFileUpdate():
  file = pathlib.Path(jsonGameFile)
  if file.exists():
    return round(time.time() - file.stat().st_mtime)
  return -1

def readGameFile():
  global data
  with open(jsonGameFile) as f:
    data = json.load(f)
    f.close()

def updateSteamFile():
  urllib.request.urlretrieve (steamGameListUrl, "steam.json")

def checkUpdateGameData():
  updateFrequency = 12 * 60 * 60 # How often to refresh the json in seconds
  file = pathlib.Path(jsonGameFile)
  if file.exists():
    timeSinceLastUpdate = time.time() - file.stat().st_mtime
    if timeSinceLastUpdate > updateFrequency:
      print("Updating file, last update {} hours ago".format(timeSinceLastUpdate/60/60))
      updateSteamFile()
      readGameFile()
  else:
    print("json not found, fetching it")
    updateSteamFile()
    readGameFile()

def findName(appid):
  for app in data["applist"]["apps"]:
    if app["appid"] == appid:
      return app["name"]
  return "Error : game not found"

def findAppId(name):
  checkUpdateGameData()
  readGameFile()
  bestMatchName = ""
  bestMatch = -1
  bestRatio = 0
  for app in data["applist"]["apps"]:
    appName = app["name"]
    searchName = name
    appId = app["appid"]
    fuzzRatio = fuzz.ratio(appName.lower(), searchName.lower())
    if fuzzRatio > bestRatio:
      bestRatio = fuzzRatio
      bestMatch = appId
      bestMatchName = appName
      if bestRatio == 100:
        break
  print("Found app {} with fuzz ratio of {}, id {}".format(bestMatchName, bestRatio, bestMatch))
  response = {"appid" : bestMatch, "name" : bestMatchName, "matchscore" : bestRatio}
  return json.dumps(response)


# while True:
#   name = input("App name to search for: ")
#   findAppId(name)

checkUpdateGameData()
