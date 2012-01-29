##############################################################################
#
# Copyright 2012 Andreas Motl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################

import sys
import re
import shlex
import subprocess
from zt.vlc import find_vlc

"""
# Parse information from STDERR, i.e.:
[0x100600e28] [dumpmeta] lua interface: name: Fish.mov
[0x100600e28] [dumpmeta] lua interface: uri: file:///System/Library/Compositions/Fish.mov
[0x100600e28] [dumpmeta] lua interface: duration: 13.266666
[0x100600e28] [dumpmeta] lua interface: meta data:
[0x100600e28] [dumpmeta] lua interface:   filename: Fish.mov
[0x100600e28] [dumpmeta] lua interface: info:
[0x100600e28] [dumpmeta] lua interface:   Stream 0
[0x100600e28] [dumpmeta] lua interface:     Display resolution: 640x480
[0x100600e28] [dumpmeta] lua interface:     Type: Video
[0x100600e28] [dumpmeta] lua interface:     Frame rate: 30
[0x100600e28] [dumpmeta] lua interface:     Codec: Motion JPEG Video (jpeg)
[0x100600e28] [dumpmeta] lua interface:     Language: English
[0x100600e28] [dumpmeta] lua interface:     Resolution: 640x480
"""

class VideoInfo(object):

    def __init__(self, videofile, vlc_bin = None):
        self.videofile = videofile
        self.vlc_bin = vlc_bin or find_vlc()
        cmd = \
            [self.vlc_bin] + \
            shlex.split('--intf lua --lua-intf dumpmeta --no-video-title --no-media-library -V dummy -A dummy') + \
            [self.videofile]
        process = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        self.stdout, self.stderr = process.communicate()

    @property
    def raw(self):
        return self.stderr

    @property
    def duration(self):
        m = re.match('.*duration: ([\d.]+).*$', self.stderr, re.DOTALL)
        if m:
            return float(m.group(1))

    @property
    def size(self):
        m = re.match('.*Resolution: ([\dx]+).*$', self.stderr, re.DOTALL)
        if m:
            return map(int, m.group(1).split('x'))
