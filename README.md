# Steam API  
- Implement fuzzy search for the appid from the app name  
- Get the current player count for a game by appid
- Adds a few endpoints that returns complete replys for twitch bots
- Very much work in progress and quickly hacked together.

## Running
`docker compose up --build`  

## Dev
To auto update dependencies : `uv lock --upgrade`  
To generate new requirements.txt from uv: `uv pip freeze > requirements.txt`  