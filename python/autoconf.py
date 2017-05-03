# -*- coding: utf-8 -*-
#
#
#

import os
import re

from fnmatch import fnmatch

try:
    import weechat as w

except Exception:
    print("This script must be run under WeeChat.")
    print("Get WeeChat now at: http://www.weechat.org/")
    quit()

NAME        = "autoconf"
AUTHOR      = "Manuel Koell <man.koell@gmail.com>"
VERSION     = "0.1"
LICENSE     = "GPL3"
DESCRIPTION = "auto save changed options as commands for FIFO pipe"

EXCLUDES = [
    '*.nicks',
    '*.username', '*.sasl_username',
    '*.password', '*.sasl_password',
    'irc.server.*.autoconnect',
    'irc.server.*.autojoin'
]

SETTINGS = {
    'autosave': ('on', 'auto save config on quit'),
    'autoload': ('on', 'auto load config on start'),
    'ignore': (
        ','.join(EXCLUDES), 
        'comma separated list of patterns to exclude'),
    'file': ('~/.weerc', 'config file location')
}

HELP = """
some helptext
"""

RE = {
    'option': re.compile('\s*(.*) = (.*)  \(default')
}


def get_config(args):
    
    try:
        conf = args[1]
    except Exception:
        conf = w.config_get_plugin('file')

    return os.path.expanduser(conf)

def cstrip(text):
    return w.string_remove_color(text, '')

def load_conf(args):
    fifo = w.info_get('fifo_filename', '')
    conf = get_config(args)

    if os.path.isfile(conf):
        w.command('', '/exec -sh -norc cat %s > %s' % (conf, fifo))

def save_conf(args=None):

    try:
        f = open(get_config(args), 'w+')

    except Exception, e:
        w.prnt('', '%sError: %s' % (w.prefix('error'), e))

        return w.WEECHAT_RC_ERROR

    header = [
        '#',
        '# WeeChat %s (compiled on %s)' % (w.info_get('version', ''), w.info_get('date', '')),
        '#',
        '# Use /autoconf load or cat this file to the FIFO pipe.',
        '#',
        '# For more info, see https://weechat.org/scripts/source/autoconf.py.html',
        '#', 
        ''
    ]

    for ln in header:
        f.write('%s\n' % ln)

    w.command('', '/buffer clear')
    w.command('', '/set diff')

    infolist = w.infolist_get('buffer_lines', '', '')

    while w.infolist_next(infolist):
        message = cstrip(w.infolist_string(infolist, 'message'))
        ignore = w.config_get_plugin('ignore').split(',')
        option = re.match(RE['option'], message)

        if option:
            if not any(fnmatch(option.group(1), p.strip()) for p in ignore):
                f.write('*/set %s %s\n' % (option.group(1), option.group(2)))

    f.close()

    w.infolist_free(infolist)

def cmd_autoconf_cb(data, buffer, args):

    args = args.split()

    if 'save' in args:
        save_conf(args)

    elif 'load' in args:
        load_conf(args)

    else:
        w.command('', '/help ' + NAME)

    return w.WEECHAT_RC_OK

if __name__ == '__main__':
    if w.register(NAME, AUTHOR, VERSION, LICENSE, DESCRIPTION, "", ""):
        w.hook_command(NAME, DESCRIPTION, 'save [path] || load [path]', HELP, 'save || load', 'cmd_autoconf_cb', '')

        for option, value in SETTINGS.items():
            if not w.config_is_set_plugin(option):
                w.config_set_plugin(option, value[0])
                w.config_set_desc_plugin(option, '%s  (default: "%s")' % (value[1], value[0]))

        if 'on' in w.config_get_plugin('autoload'):
            load_conf(None)

        if 'on' in w.config_get_plugin('autosave'):
            w.hook_signal('quit', 'save_conf', '')


