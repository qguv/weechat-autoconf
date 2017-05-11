# weechat-autoconf

auto save the diff of changed options as commands for the FIFO pipe

## Install

`/script install autoconf.py`

## Options
* `plugins.var.python.autoconf.autoload`: auto load config on start  (default: "on")
* `plugins.var.python.autoconf.autosave`: auto save config on quit  (default: "on")
* `plugins.var.python.autoconf.file`: path to config file  (default: "~/.weerc")
* `plugins.var.python.autoconf.ignore`: comma separated list of patterns to exclude

## Ignore

Usually you want to make sure to exclude sensitive information such as nicks, usernames, passwords and the like. Thus it ignores the following patterns by default:

```
*.nicks,
*.username, *.sasl_username,
*.password, *.sasl_password,
irc.server.*.autoconnect,
irc.server.*.autojoin
```

