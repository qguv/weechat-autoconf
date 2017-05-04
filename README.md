# weechat-autoconf

auto save the diff of changed options as commands for the FIFO pipe

## Install

Once the script is [approved](https://weechat.org/scripts/pending/), it will be as easy as `/script install autoconf.py`. In the meantime you need to clone this repo, put a symlink into weechat's python folder and load the script manually with `/script load autoconf.py`.

## Options
* `plugins.var.python.autoconf.autoload`: auto load config on start  (default: "on")
* `plugins.var.python.autoconf.autosave`: auto save config on quit  (default: "on")
* `plugins.var.python.autoconf.file`: path to config file  (default: "~/.weerc")
* `plugins.var.python.autoconf.ignore`: comma separated list of patterns to exclude

## Ignore

Usually you want to make sure to exclude sensitive information such as nicks, usernames, passwords and the like. Thus the config file ignores the following default patterns:

```
*.nicks,
*.username, *.sasl_username,
*.password, *.sasl_password,
irc.server.*.autoconnect,
irc.server.*.autojoin
```

