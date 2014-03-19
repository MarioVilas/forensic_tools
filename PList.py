# Property List encoding and decoding
# by Mario Vilas (mvilas at gmail.com)

# Copyright (c) 2009-2012, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#------------------------------------------------------------------------------
# Imports

import types
import base64
import string
import datetime
from xml.etree import ElementTree

#------------------------------------------------------------------------------
# Exports

__all__ = [

    # Static class containing all the methods.
    "PList",

    # User interface.
    "parse",
    "fromstring",
    "fromtree",
    "dump",
    "tostring",
    "totree",
    "fromfile",
    "tofile",
]

#------------------------------------------------------------------------------
# Public methods

class PList:
    """
    Static class to parse C{.plist} files to native Python types and back.

    Example 1: parsing the sample file from the plist man pages::
        >>> from PList import *
        >>> example = \"\"\"
        ... <?xml version="1.0" encoding="UTF-8"?>
        ... <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
        ...         "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        ... <plist version="1.0">
        ... <dict>
        ...     <key>Year Of Birth</key>
        ...     <integer>1965</integer>
        ...     <key>Pets Names</key>
        ...     <array/>
        ...     <key>Picture</key>
        ...     <data>
        ...         PEKBpYGlmYFCPA==
        ...     </data>
        ...     <key>City of Birth</key>
        ...     <string>Springfield</string>
        ...     <key>Name</key>
        ...     <string>John Doe</string>
        ...     <key>Kids Names</key>
        ...     <array>
        ...         <string>John</string>
        ...         <string>Kyra</string>
        ...     </array>
        ... </dict>
        ... </plist>
        \"\"\"
        >>> data = fromstring(example)
        >>> data
        {'Pets Names': [], 'Kids Names': ['John', 'Kyra'], 'Picture': '<B\x81\xa5\x81\xa5\x99\x81B<', 'Year Of Birth': 1965, 'City of Birth': 'Springfield', 'Name': 'John Doe'}
        >>> tostring(data) == example   # False, as this is not guaranteed.
        False

    Example 2: creating a new C{.plist} file from scratch::
        >>> a = dict()
        >>> a["hello"] = "world"
        >>> a["a boolean"] = True
        >>> a["an integer"] = 5
        >>> a["a float"] = 1.0
        >>> a["a non printable string"] = "\0\1\2\3\4\5\6"
        >>> a["a dictionary"] = dict()
        >>> a["a dictionary"]["example"] = "nesting"
        >>> a["a list"] = [0,1,2,3,4,5]
        >>> a["nested lists"] = [ ["are", "possible"], "too", ["of", "course"] ]
        >>> a
        {'a boolean': True, 'an integer': 5, 'a list': [0, 1, 2, 3, 4, 5], 'nested lists': [['are', 'possible'], 'too', ['of', 'course']], 'a non printable string': '\x00\x01\x02\x03\x04\x05\x06', 'a float': 1.0, 'hello': 'world', 'a dictionary': {'example': 'nesting'}}
        >>> from PList import *
        >>> b = tostring(a)
        >>> a == fromstring(b)
        True
        >>> print b,
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
               "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict><key>a boolean</key>
        <true />
        <key>a dictionary</key>
        <dict><key>example</key>
        <string>nesting</string>
        </dict>
        <key>a float</key>
        <real>1.0</real>
        <key>a list</key>
        <array><integer>0</integer>
        <integer>1</integer>
        <integer>2</integer>
        <integer>3</integer>
        <integer>4</integer>
        <integer>5</integer>
        </array>
        <key>a non printable string</key>
        <data>AAECAwQFBg==</data>
        <key>an integer</key>
        <integer>5</integer>
        <key>hello</key>
        <string>world</string>
        <key>nested lists</key>
        <array><array><string>are</string>
        <string>possible</string>
        </array>
        <string>too</string>
        <array><string>of</string>
        <string>course</string>
        </array>
        </array>
        </dict>
        </plist>
"""

    @classmethod
    def parse(self, filename):
        """
        Read a C{.plist} file from disk and return its contents using builtin
        Python types.

        @type  filename: str
        @param filename: Name of the file to read.

        @return: Contents of the file. May be any combination of the following
            builtin types:
             * dict
             * list
             * str
             * int
             * long
             * float
             * bool
        """
        return self.fromtree( ElementTree.parse(filename) )

    @classmethod
    def fromstring(self, stringdata):
        """
        Parse the contents of a C{.plist} file in the given string and return
        its contents using builtin Python types.

        @type  stringdata: str
        @param stringdata: File contents to parse.

        @return: Contents of the file. May be any combination of the following
            builtin types:
             * dict
             * list
             * str
             * int
             * long
             * float
             * bool
        """
        return self.fromtree( ElementTree.fromstring( stringdata.strip() ) )

    @classmethod
    def fromtree(self, xml):
        """
        Parse the contents of a C{.plist} file in the given ElementTree node
        and return its contents using builtin Python types.

        @type  xml: xml.etree.ElementTree.Element
        @param xml: Any node in the tree. Parsing will always begin from the
            root node, regardless of which node you pass to this function.

        @return: Contents of the file. May be any combination of the following
            builtin types:
             * dict
             * list
             * str
             * int
             * long
             * float
             * bool
        """
        if hasattr(xml, 'getroot'):
            xml = xml.getroot()
        children = xml.getchildren()
        if xml.tag != 'plist' or len(children) != 1:
            raise Exception, "Bad property list"
        return self.__build(children[0])

    @classmethod
    def dump(self, filename, plist):
        """
        Marshall the given data and write it into a C{.plist} file.

        @warn: If the file already exists, its contents will be replaced.

        @note: In all platforms the end of line sequence will be C{"\n"},
            even in Windows which normally uses C{"\r\n"} instead.

        @type  filename: str
        @param filename: Name of the file to write.

        @param plist: Contents of the file.  May be any combination of the
            following builtin types:
             * dict
             * list
             * str
             * int
             * long
             * float
             * bool
        """
        xml = self.tostring(plist)
        fd = open(filename, 'wb')
        try:
            fd.write(xml)
        finally:
            fd.close()

    @classmethod
    def tostring(self, plist):
        """
        Marshall the given data in C{.plist} file format.

        @param plist: Contents of the file.  May be any combination of the
            following builtin types:
             * dict
             * list
             * str
             * int
             * long
             * float
             * bool

        @rtype:  str
        @return: Marshalled data in XML (C{.plist}) format.
        """
        xml  = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"\n'
        xml += '       "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        xml += '<plist version="1.0">\n'
        xml += self.__marshall(plist)
        xml += '</plist>\n'
        return xml

    @classmethod
    def totree(self, plist):
        """
        Convert the given data to an ElementTree tree in C{.plist} file format.

        @param plist: Contents of the file.  May be any combination of the
            following builtin types:
             * dict
             * list
             * str
             * int
             * long
             * float
             * bool

        @rtype:  xml.etree.ElementTree.Element
        @return: Marshalled data in XML (C{.plist}) format.
        """
        xml  = self.tostring(plist)
        tree = ElementTree.fromstring(xml)
        return tree

    fromfile    = parse
    tofile      = dump

#------------------------------------------------------------------------------
# Internally used worker methods and classes

    @classmethod
    def __marshall(self, data):
        classname       = self.__name__
        typename        = data.__class__.__name__
        marshaller_name = '_%s__marshall_%s' % (classname, typename)
        if not hasattr(self, marshaller_name):
            raise KeyError, marshaller_name
##            marshaller  = self.__marshall_string
        else:
            marshaller  = getattr(self, marshaller_name)
        return marshaller(data)

    @classmethod
    def __build(self, element):
        classname       = self.__name__
        typename        = element.tag
        builder_name    = '_%s__build_%s' % (classname, typename)
        if not hasattr(self, builder_name):
            raise KeyError, builder_name
##            builder     = self.__build_string
        else:
            builder     = getattr(self, builder_name)
        return builder(element)

    @staticmethod
    def __properties(element):
        props = {}
        for key, value in element.items():
            props[key] = value
        return props

    # TO DO: it would be nice to output indented tags.
    @staticmethod
    def __tag(name, value = '', props = {}):
        value = str(value)
        props = ''.join( [ (' %s="%s"' % p) for p in props.iteritems() ] )
        if value:
            return '<%(name)s%(props)s>%(value)s</%(name)s>\n' % vars()
        return '<%(name)s%(props)s />\n' % vars()

#------------------------------------------------------------------------------
# Marshallers

    @classmethod
    def __marshall_dict(self, data):
        m    = ''
        tags = data.keys()
        tags.sort()
        for key in tags:
            value = data[key]
            m    += self.__tag('key', key) + self.__marshall(value)
        return self.__tag('dict', m)

    @classmethod
    def __marshall_list(self, data):
        children = ''.join([ self.__marshall(element) for element in data ])
        return self.__tag('array', children)

    __marshall_tuple = __marshall_list

    @classmethod
    def __marshall_NoneType(self, data):
        return self.__tag('undef', '')

    @classmethod
    def __marshall_bool(self, data):
        if data:
            return self.__tag('true')
        return self.__tag('false')

    # XXX python only supports floats, we need doubles
    @classmethod
    def __marshall_float(self, data):
        return self.__tag('real', repr(data))

    @classmethod
    def __marshall_int(self, data):
        return self.__tag('integer', data)

    __marshall_long = __marshall_int

    __printables = set(string.printable)

    @classmethod
    def __marshall_str(self, data):
        if set(data).issubset(self.__printables):
            return self.__tag('string', data)
        return self.__marshall_buffer(data)

    @classmethod
    def __marshall_buffer(self, data):
        data = base64.encodestring(str(data))
        data = data.replace('\n', '')
        data = data.replace('\r', '')
        data = data.strip()
        return self.__tag('data', data)

    @classmethod
    def __marshall_date(self, data):
        return self.__tag('date', str(d))

#------------------------------------------------------------------------------
# Builders

    @classmethod
    def __build_dict(self, element):
        data     = {}
        children = element.getchildren()
        if (len(children) & 1) != 0:
            raise IndexError, "Incomplete dictionary"
        for index in range(0, len(children), 2):
            key     = children[index]
            value   = children[index + 1]
            if key.tag != 'key':
                raise ValueError, "Bad dictionary data"
            data[key.text] = self.__build(value)
        return data

    @classmethod
    def __build_array(self, element):
        return [ self.__build(child) for child in element.getchildren() ]

    @staticmethod
    def __build_undef(element):
        return None

    @staticmethod
    def __build_true(element):
        return True

    @staticmethod
    def __build_false(element):
        return False

    # XXX python only supports floats, we need doubles
    @staticmethod
    def __build_real(element):
        return float(element.text)

    @staticmethod
    def __build_integer(element):
        try:
            return int(element.text)
        except ValueError:
            return long(element.text)

    @staticmethod
    def __build_string(element):
        return element.text

    @classmethod
    def __build_data(self, element):
        return base64.decodestring(str(element.text))

    @classmethod
    def __build_date(self, element):
        return datetime.fromtimestamp(str(element.text))

#------------------------------------------------------------------------------
# User interface

parse       = PList.parse
fromstring  = PList.fromstring
fromtree    = PList.fromtree
dump        = PList.dump
tostring    = PList.tostring
totree      = PList.totree
fromfile    = PList.fromfile
tofile      = PList.tofile

#------------------------------------------------------------------------------
# Test code

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        plist = fromfile(filename)
    else:
        data = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
        "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Year Of Birth</key>
    <integer>1965</integer>
    <key>Pets Names</key>
    <array/>
    <key>Picture</key>
    <data>
        PEKBpYGlmYFCPA==
    </data>
    <key>City of Birth</key>
    <string>Springfield</string>
    <key>Name</key>
    <string>John Doe</string>
    <key>Kids Names</key>
    <array>
        <string>John</string>
        <string>Kyra</string>
    </array>
</dict>
</plist>
"""
        plist = fromstring(data)

    print plist
    print '-' * 79

    xml = tostring(plist)
    print xml
