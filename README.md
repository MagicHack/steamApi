# Steam API  
- Implement fuzzy search for the appid from the app name  
- Get the current player count for a game by appid
- Adds a few endpoints that returns complete replys for twitch bots
- Very much work in progress and quickly hacked together.
- Install instructions maybe to come, but it's basically https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04 you also need to `pip install fuzzywuzzy[speedup]` in your venv.
- run updateSteamGames.sh to get the json containing the game list or to update it
