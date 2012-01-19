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
import logging
from opterator import opterate
from string import Template
from tempfile import NamedTemporaryFile
import subprocess
import time

logger = logging.getLogger(__name__)

class VideoTwister(object):

    def __init__(self, **kwargs):
        self.options = kwargs
        self.autoconfig()

    def autoconfig(self):

        if not self.options.get('vlc'):
            self.options['vlc'] = '/Applications/VLC.app/Contents/MacOS/VLC'
        if self.options.has_key('maskfile') and not self.options.get('maskwidth') and not self.options.get('maskheight'):
            self.options['maskwidth'], self.options['maskheight'] = self.mask_size

        self.options['masksize'] = ''
        if self.options.has_key('maskwidth'):
            self.options['masksize'] += 'width=' + str(self.options['maskwidth']) + ','
        if self.options.has_key('maskheight'):
            self.options['masksize'] += 'height=' + str(self.options['maskheight']) + ','

        self.options['display'] = self.options['watch'] and ':display' or ''
        self.options['verbose'] = self.options['verbose'] and '-vv' or ''

    def overlay(self, vlm_template):
        logger.debug("VLM options: %s" % self.options)
        with open(vlm_template) as f:
            tpl = Template(f.read())
            vlmdata = tpl.safe_substitute(self.options)
            logger.debug("VLM data: %s" % vlmdata)
            vlmfile = NamedTemporaryFile(delete=False)
            vlmfile.write(vlmdata)
            vlmfile.flush()

            #cmd = [self.options['vlc'], '-I', 'dummy', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
            #cmd = [self.options['vlc'], '-I', 'telnet', '--telnet-password', 'test', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
            #cmd = [self.options['vlc'], '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
            #cmd = [self.options['vlc'], '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], 'vlc://pause:2', 'vlc://quit']
            cmd = [self.options['vlc'], '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], 'vlc://quit']
            #cmd = [self.options['vlc'], '-I', 'macosx', '-I', 'telnet', '--telnet-password', 'test', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
            # 'vlc://quit'
            self.run_process(cmd)

    def run_process(self, args, success_duration_threshold=5):
            #logger.info("VLC command: %s" % (' '.join(cmd)))
            command = ' '.join(args)
            logger.info("VLC command: %s" % command)
            #print os.system(command)
            #return
            #"""
            begin = time.time()
            #process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process = subprocess.Popen(args)
            #process = subprocess.Popen(cmd, close_fds=True, shell=True)
            #process = subprocess.Popen(command + ' -I macosx', shell=True)
            #process = subprocess.Popen(command)
            stdout, stderr = process.communicate()
            finish = time.time()

            duration = finish - begin
            success = process.returncode == 0 or duration >= success_duration_threshold
            
            if success:
                logger.info("VLC finished successfully")
            else:
                logger.error("VLC failed: stdout=%s, stderr=%s" % (stdout, stderr))
            #"""

    def overlay_videos(self):
        tplfile = os.path.join(os.path.dirname(__file__), 'overlay_videos.vlm.tpl')
        return self.overlay(tplfile)

    @property
    def mask_size(self):
        from PIL import Image
        image = Image.open(self.options.get('maskfile'))
        return image.size

def setup_logging():
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    logger = logging.getLogger(__name__)
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)

@opterate
def main(output, background, overlay, angle=45, maskfile='', watch=False,
        vlc=None, verbose=False):
    """
    An example copy script with some example parameters that might
    be used in a copy command.
    
    @param angle -a --angle which angle to rotate the overlay (default: 0)
    @param maskfile -m --mask overlay alpha mask image
    @param watch -w --watch whether to display the result in vlc or not (default: false)
    @param vlc -V --vlc path to vlc executable
    @param verbose -v --verbose verbose
    """

    setup_logging()
    logger.info("zt.vlc.twister starting")
    options = locals()
    options.update({'output': output, 'background': background, 'overlay': overlay})
    twister = VideoTwister(**options)
    twister.overlay_videos()

if __name__ == '__main__':
    main()
