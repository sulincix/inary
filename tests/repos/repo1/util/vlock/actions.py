#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from inary.actionsapi import autotools
from inary.actionsapi import inarytools
from inary.actionsapi import get

def setup():
    autotools.rawConfigure("--prefix=/usr \
                            --bindir=/usr/bin \
                            --sbindir=/usr/sbin \
                            --libdir=/usr/lib \
                            --mandir=/usr/share/man")

def build():
    autotools.make('CC=%s CFLAGS="%s -std=gnu99"' % (get.CC(), get.CFLAGS()))

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    inarytools.dodoc("ChangeLog", "COPYING", "PLUGINS", "README*", "SECURITY", "STYLE", "TODO")

