# -*- coding: utf-8 -*-
#
# Main fork Pisi: Copyright (C) 2005 - 2011, Tubitak/UEKAE (Licensed with GPLv2)
# More details about GPLv2, please read the COPYING.OLD file.
#
# Copyright (C) 2016 - 2019, Suleyman POYRAZ (Zaryob)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# Please read the COPYING file.
#


"""
 XmlFile class further abstracts a dom object using the
 high-level dom functions provided in xmlext module (and sorely lacking
 in xml.dom :( )

 function names are mixedCase for compatibility with iksemel,
 an 'old library'

 this implementation uses iksemel
"""

import gettext

__trans = gettext.translation('inary', fallback=True)
_ = __trans.gettext

import io
import ciksemel as iks

import inary.errors
import inary.config
from inary.file import File


class Error(inary.errors.Error):
    pass


class XmlFile(object):
    """A class to help reading and writing an XML file"""

    def __init__(self, tag):
        self.rootTag = tag

    def newDocument(self):
        """clear DOM"""
        self.doc = iks.newDocument(self.rootTag)

    def unlink(self):
        """deallocate DOM structure"""
        del self.doc

    def rootNode(self):
        """returns root document element"""
        return self.doc

    def parsexml(self, file):
        try:
            if type(file) == bytes:
                file.decode('utf-8')
            self.doc = iks.parseString(str(file))
            return self.doc
        except Exception as e:
            raise Error(_("File \"{}\" has invalid XML: {}").format(file, e))

    def readxml(self, uri, tmpDir='/tmp', sha1sum=False,
                compress=None, sign=None, copylocal=False):
        uri = File.make_uri(uri)
        try:
            localpath = File.download(uri, tmpDir, sha1sum=sha1sum,
                                      compress=compress, sign=sign, copylocal=copylocal)
        except IOError as e:
            raise Error(_("Cannot read URI {0}: {1}").format(uri, str(e)))

        st = io.StringIO()

        try:
            from inary.libraries.preprocess import preprocess
            preprocess.preprocess(infile=localpath, outfile=st, defines=inary.config.Config().values.directives)
            st.seek(0)
        except:
            st = open(localpath)

        try:
            self.doc = iks.parse(localpath)
            return self.doc
        except Exception as e:
            raise Error(_("File \"{}\" has invalid XML").format(localpath))

    def writexml(self, uri, tmpDir='/tmp', sha1sum=False, compress=None, sign=None):
        f = File(uri, File.write, sha1sum=sha1sum, compress=compress, sign=sign)
        f.write(self.doc.toPrettyString())
        f.close()

    def writexmlfile(self, f):
        f.write(self.doc.toPrettyString())
