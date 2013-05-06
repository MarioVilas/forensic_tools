#!/usr/bin/python

# Strip subfiles using the output of hachoir-subfile
# by Mario Vilas (mvilas at gmail.com)

# Copyright (c) 2008-2013, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import re
import os
import sys

# [+] File at 955391488 size=2863284 (2.7 MB): JPEG picture

# last file has to be recovered by hand

# pos, size, type
parser = re.compile('\[\+\] File at ([0-9]+) size\=([0-9]+) \([^\)]+\)\: (.*)')

file_types = {
    'JPEG'          :   'jpg',
#    'executable'    :   'exe',
    'AVI'           :   'avi',
#    '7z'            :   '7z',
#    'iTunesDB'      :   'db',
}

src_fd = open(sys.argv[1], 'rb')
while 1:
    line = sys.stdin.readline()
    if not line: break
    m = parser.search(line)
##    print line
##    print m
    if m:
##        print m.groups()
        fpos, fsize, ftype = m.groups()
        fpos, fsize = long(fpos), long(fsize)
##        print fpos, fsize, ftype
        if fpos > 0 and fsize > 0:
            fext = 'bin'
            for ft_test in file_types.keys():
                if ft_test in ftype:
                    fext = file_types[ft_test]
                    break
            fname = 'file%x.%s' % (fpos, fext)
            if fext == 'bin':
                print "SKIPPED", fname, fpos, fsize, ftype
                continue
            print "writing", fname, fpos, fsize, ftype
            dst_fd = open(fname, 'wb')
            dst_fd.seek(0, os.SEEK_SET)
            src_fd.seek(fpos, os.SEEK_SET)
            while fsize > 0:
                buff = src_fd.read(min(0x10000, fsize))
                fsize = fsize - len(buff)
                while buff:
                    bw = dst_fd.write(buff)
                    if not bw: break
                    buff = buff[bw:]
            dst_fd.close()
src_fd.close()
