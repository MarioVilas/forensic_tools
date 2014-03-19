#!/usr/bin/env python

# Copyright (c) 2009-2012, Mario Vilas
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

from __future__ import with_statement

from glob import glob
from sys import exit

print "Whatsapp msgstore decoder"
print "By Mario Vilas (mvilas at gmail dot com)"
print

try:
    from Crypto.Cipher import AES
except ImportError:
    print "Error: PyCrypto is required to run this tool."
    print
    print "On Ubuntu you can install it with the following command:"
    print "    sudo apt-get install python-crypto"
    exit(1)

KEY = ('\x34\x6a\x23\x65\x2a\x46\x39\x2b\x4d\x73\x25\x7c'
       '\x67\x31\x7e\x35\x2e\x33\x72\x48\x21\x77\x65\x2c')
CIPHER = AES.new(KEY, 1)

names = glob('msgstore*.db.crypt')
if not names:
    print "Error: No encrypted Whatsapp message store found here!"
    exit(1)

for old_name in names:
    new_name = old_name[:-6]
    with open(old_name, 'rb') as fd:
        data = fd.read()
    data = CIPHER.decrypt(data)
    with open(new_name, 'wb') as fd:
        fd.write(data)
    del data
    print "Decoded %r as %r" % (old_name, new_name)

print
print "Done decoding %d files." % len(names)
exit(0)
