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
import time
import logging
import subprocess
import threading
from tempfile import NamedTemporaryFile
from zt.vlc import find_vlc
from zt.util.tail import Monitor

logger = logging.getLogger(__name__)


class VlcRunner(object):
    """Run VLC"""

    def __init__(self, command_args, vlc_bin=None, timeout=120, \
        verbose=False, debug=False, error_on_segfault=True):

        # specific command line arguments to pass to VLC
        self.command_args = command_args

        # path to the VLC executable
        self.vlc_bin = vlc_bin or find_vlc()

        # say something?
        self.verbose = verbose

        # do something to support debugging the underlying VLC
        self.debug = debug

        # the subprocess reference
        self.process = None

        # the subprocess will be started in another thread
        self.thread = None

        # for timing out the operation
        self.timer = None
        self.timeout = timeout

        # indicates whether we are currently terminating ourselves regularly
        self.terminating = False
        # indicates whether a timeout occurred
        self.timeout_occurred = False

        # for monitoring VLC's log file
        self.logmonitor = None
        self.logfile = NamedTemporaryFile(delete=not self.debug)

        # time keeping
        self.begin = 0
        self.finish = 0

        # whether processing was successful
        self.success = None

        # whether to error or warn on segfault
        self.error_on_segfault = error_on_segfault

    def start(self):
        """Start process runner thread and timer for timeout."""
        self.thread = threading.Thread(target=self.run_process)
        self.thread.start()
        self.timer = threading.Timer(self.timeout, self.stop_timeout)
        self.timer.start()

    @property
    def command(self):
        """Prepare to run the VLC process:
            - Compute real VLC command line arguments

        """
        base_options = [
            '--play-and-exit',
            '--no-video-title', '--no-media-library',
            '--no-sub-autodetect-file',
            '--no-sout-transcode-hurry-up', '--no-drop-late-frames',
            '--no-skip-frames', '--no-autoscale',
        ]
        logging_options = [
            '--file-logging', '--logfile', self.logfile.name,
            # --verbose-objects=+input,-all
            '--log-verbose', '3',
            '--verbose-objects', '-all,+main,+mux_ps,+access_output_file',
        ]

        extra_options = []
        if self.verbose:
            extra_options += ['--verbose', '2']
        else:
            extra_options += ['--quiet']

        cmd = [self.vlc_bin] + base_options + logging_options + \
            extra_options + self.command_args
        #cmd += ['vlc://quit']

        return cmd

    def run_process(self):
        """Actually run the VLC process:
            - Start logfile monitor
            - Run VLC for video processing
            - Wait for video processing to finish

        """

        command = self.command

        logmethod = self.debug and logger.info or logger.debug
        logmethod("VLC command: %s" % ' '.join(command))
        self.begin = time.time()

        # start VLC
        popenargs = {}
        if not self.verbose:
            popenargs.update({
                'stdout': subprocess.PIPE,
                'stderr': subprocess.PIPE,
            })
        self.process = subprocess.Popen(command, **popenargs)

        # watch VLC's logfile for this line, then kill it
        # some possible exit messages:
        #   - mux_ps: Close
        #   - main debug: dead input
        #   - main vlm daemon error: Load error on line 32:
        #                                       setup: Wrong command syntax
        #   - main libvlc warning: error while loading the configuration file
        def found(line):
            self.stop()
        self.logmonitor = Monitor(self.logfile.name, "mux_ps: Close", found)

        # wait for process to finish
        self.process.communicate()
        self.returncode = self.process.returncode
        self.finish = time.time()

        # exit code: 15=terminate, 9=kill
        self.success = \
            (self.returncode == 0) \
            or (self.terminating and self.returncode in [-9, -15])

        self._log_outcome()
        self._shutdown()

    def _log_outcome(self):

        if self.success and not self.timeout_occurred:
            outcome_msg = 'VLC finished successfully'
            if self.returncode in [-9, -15]:
                analysis = '[terminated-on-purpose]'
            else:
                analysis = ''
            logmethod = logger.info
        else:
            outcome_msg = 'VLC failed'
            if self.returncode == -11:
                analysis = '[segfault]'
            else:
                analysis = ''
            if self.error_on_segfault:
                logmethod = logger.error
            else:
                logmethod = logger.warn

        duration = self.finish - self.begin
        outcome_info = "returncode=%s, duration=%02ds" % \
            (self.returncode, duration)
        logmethod("%s: %s   %s" % (outcome_msg, outcome_info, analysis))

    def complete(self):
        """Wait for process runner thread to finish.

        Returns:
            the unix exit status of the process

        """
        self.thread.join()
        return self.returncode

    def stop(self, regular=True):
        """Stop VLC:

            - shuts down internal infrastructure (log monitor, time)
            - try to terminate the process
            - wait a second
            - try to kill the process

        """
        self._shutdown()
        if regular:
            self.terminating = True
        try:
            self.process.terminate()
            time.sleep(1)
            try:
                self.process.kill()
            except:
                pass
        except OSError, ex:
            logger.warn("Terminating VLC failed: %s" % ex)

    def stop_timeout(self):
        """Stop VLC indicating a timeout occurred."""

        self.timeout_occurred = True
        logger.error('VLC timed out after %s seconds' % self.timeout)
        self.stop(regular=False)

    def _shutdown(self):
        self.logmonitor.quit()
        self.timer.cancel()


class VlcSafeRunner(object):
    """
    VLC segfaults (exit code 11) really often when
    doing alpha compositing on Mac OS X - WTF!?
    This runner will compensate this issue.
    """

    def __init__(self, *args, **kwargs):
        self.args = args

        # the 'segfaults' kwarg belongs to us:
        # extract and remove it from kwargs dictionary
        kwargs.setdefault('segfaults', 20)
        self.segfaults = kwargs['segfaults']
        del kwargs['segfaults']

        kwargs['error_on_segfault'] = False

        self.kwargs = kwargs

    def start(self):
        logger.info("VlcSafeRunner: Compensating a maximum of %s segfaults" \
            % self.segfaults)
        for i in range(self.segfaults):
            vlcrunner = VlcRunner(*self.args, **self.kwargs)
            vlcrunner.start()
            returncode = vlcrunner.complete()
            if returncode != -11:
                logger.info("VlcSafeRunner: Compensated %s segfaults" % i)
                return
        logger.error("VlcSafeRunner: Failed after %s segfaults" % \
            self.segfaults)
