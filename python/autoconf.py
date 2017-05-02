# -*- coding: utf-8 -*-
#
#
#

import os
import re

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

HELP = """
some helptext
"""

def cstrip(text):
    return w.string_remove_color(text, '')

def load_conf():
    pass

def save_conf(conf):
    w.command('', '/buffer clear')
    w.command('', '/set diff')

    infolist = w.infolist_get('buffer_lines', '', '')
    version = w.info_get('version', '')

    try:
        f = open(conf, 'w+')
    except e:
        w.prnt('error: %s' % e)

    while w.infolist_next(infolist):
        message = cstrip(w.infolist_string(infolist, 'message'))
        f.write('%s \n' % message)

    w.infolist_free(infolist)
    f.close()

def cmd_autoconf_cb(data, buffer, args):

    args = args.split()
    conf = os.path.expanduser('~/.weerc')

    if 'save' in args:
        save_conf(conf)

    elif 'load' in args:
        load_conf()

    else:
        # w.command('', '/help ' + NAME)
        pass

    return w.WEECHAT_RC_OK

if __name__ == '__main__':
    if w.register(NAME, AUTHOR, VERSION, LICENSE, DESCRIPTION, "", ""):
        w.hook_command(NAME, DESCRIPTION, 'save [path] || load [path]', HELP, 'save || load', 'cmd_autoconf_cb', '')


