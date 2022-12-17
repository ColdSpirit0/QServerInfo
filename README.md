# QServerInfo

Shows info about quake servers in the tray

### How to install (linux only)

```shell
pip install qserverinfo
```


### Usage

```shell
qserverinfo [IP]:[PORT]
```

### Additional arguments:

```
-n NAME, --name NAME  server name, it will be shown in GUI
-it ICON_TITLE, --icon-title ICON_TITLE
                    text on top of icon
-rd REQUEST_DELAY, --request-delay REQUEST_DELAY
                    how often server will be requested; in seconds, minimum 30, default 60
-fb, --filter-bots    remove bots from players count if possible
-e EXECUTABLE, --executable EXECUTABLE
                    path to game executable which will start after "Join" button click with parameter "+connect <address>"
-m, --show-mapname    display mapname in the window if possible
```

### Supported games

Possibly all games that supported by https://github.com/cetteup/pyq3serverlist

**What I tested and its working:**

- Xonotic 
- OpenArena
- Warsow
- Doombringer

**Not working:**

- QuakeWorld
- AlienArena
