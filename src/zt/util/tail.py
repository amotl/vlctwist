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

import os, sys
import time
from threading import Thread

class Tail(object):
    """
    Python implementation of UNIX tail.
    Non-blocking by using threading with callbacks.

    Blueprint:
        - http://stackoverflow.com/questions/8588147/using-python-how-to-execute-this-code-concurrently-for-multiple-files/8589113#8589113

    Enhancements:
        - object oriented
        - configurable callback function
        - quit() functionality

    See also:
        - http://code.activestate.com/recipes/157035/
        - http://pypi.python.org/pypi/tailer/

    """

    def __init__(self, filename, callback, out = None):
        """
        Create Tail object

        Arguments:
            filename -- file to tail
            callback -- will be called for each line

        Keyword arguments:
            out      -- a writable stream, lines will be printed to (for debugging)

        """
        self.filename = filename
        self.callback = callback
        self.out = out
        self.killswitch = False
        self.thread = Thread(target = self.logtail)
        self.thread.start()

    def logtail(self):
        """
        Thread entrypoint:
            - starts following
            - optionally prints line to output stream
            - triggers callback

        """
        for line in self.follow():
            if self.out:
                self.out.write('tail: ')
                self.out.write(line)
            self.callback(line)

    def follow(self):
        """
        Generator to follow a file in an
        endless loop emitting each line.
        Exits if killswitch is triggered.

        """
        with open(self.filename) as file:
            file.seek(0, os.SEEK_END)
            while True:
                if self.killswitch:
                    break
                for line in iter(file.readline, ''):
                    yield line
                time.sleep(1)

    def quit(self):
        """Triggers killswitch"""
        self.killswitch = True


class Monitor(object):
    """
    Monitor file for occurrence of pattern - on top of Tail.

    """

    def __init__(self, filename, pattern, callback, out = None):
        """
        Create Monitor object, start underlying Tail

        Arguments:
            filename -- file to monitor
            pattern  -- pattern to search for
            callback -- will be called for each line

        Keyword arguments:
            out      -- a writable stream, lines will be printed to (for debugging)

        """
        self.pattern = pattern
        self.callback = callback
        self.tail = Tail(filename, self.check_line, out)
    
    def check_line(self, line):
        """
        If pattern matched, quit monitor and call callback
        TODO: enhance dumb "contains" comparison by regex matching

        """
        if self.pattern in line:
            self.quit()
            self.callback(line)

    def quit(self):
        """Quit underlying Tail"""
        self.tail.quit()
