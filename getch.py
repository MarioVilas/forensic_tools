# Cross platform getch() and putch() implementation
# by Mario Vilas (mvilas at gmail.com)
# based on http://snippets.dzone.com/posts/show/915

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

__all__ = [ 'getch', 'putch' ]

import select
import socket
import os
import sys
import time

try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import tty
except ImportError:
    tty = None

try:
    import termios
except ImportError:
    termios = None

class Getch:

    def __init__( self ):
        if msvcrt != None:
            self.getch = self.getch_windows
        elif tty != None and termios != None:
            self.getch = self.getch_unix
        else:
            raise Exception, "Unknown target OS"

    def getch_unix( self ):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr( fd )
        try:
            tty.setraw( sys.stdin.fileno() )
            ch = sys.stdin.read( 1 )
        finally:
            termios.tcsetattr( fd, termios.TCSADRAIN, old_settings )
        return ch

    def getch_windows( self ):
        ch = msvcrt.getch()
        if ch == '\r':
            ch = '\r\n'
        return ch

getch = Getch().getch

def putch( ch ):
    sys.stdout.write( ch )
    sys.stdout.flush()

if __name__ == '__main__':
    while 1:
        putch( getch() )
