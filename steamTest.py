import json
import sys
from fuzzywuzzy import fuzz

with open('steam.json') as f:
  data = json.load(f)
  f.close()
# print(data["applist"]["apps"])

def findName(appid):
  for app in data["applist"]["apps"]:
    if app["appid"] == appid:
      return app["name"]
  return "Error : game not found"

def findAppId(name):
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
