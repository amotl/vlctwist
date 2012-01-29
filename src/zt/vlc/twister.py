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
import logging
from string import Template
from tempfile import NamedTemporaryFile
from opterator import opterate
from PIL import Image

from zt.vlc.runner import VlcRunner, VlcSafeRunner
from zt.vlc.videoinfo import VideoInfo
from zt.graphics.alpha import AlphaMask

logger = logging.getLogger(__name__)

class VideoTwisterBase(object):

    def __init__(self, **kwargs):
        """Create VideoTwister.

        Keyword arguments:
            * -- all keyword arguments will be propagated to the VLM template

        """
        self.options = kwargs
        self.mungle_options()

    def run_vlc_with_vlm(self, vlm_template):
        """Process VLM template and start VLC with it."""

        logger.debug("VLM options: %s" % self.options)
        with open(vlm_template) as f:

            # interpolate options into VLM template
            vlmdata = Template(f.read()).safe_substitute(self.options)
            vlmdata = Template(vlmdata).safe_substitute(self.options)

            # write VLM file to disk
            vlmfile = NamedTemporaryFile(delete = not self.options['debug'])
            vlmfile.write(vlmdata)
            vlmfile.flush()

            logger.debug("VLM file (%s):\n%s" % (vlmfile.name, vlmdata))

            # compute VLC options
            args = ['--vlm-conf', vlmfile.name]
            if not self.options['watch']:
                args += ['--intf', 'dummy']

            # run VLC
            #vlc = VlcRunner(cmd, self.options['vlc'], verbose = self.options['verbose'])

            # run VLC, retrying some more for compensating segfaults when doing alpha compositing - WTF!?
            vlc = VlcSafeRunner(
                args,
                vlc_bin = self.options['vlc'],
                segfaults = self.options['segfaults'],
                timeout = self.options['timeout'],
                verbose = self.options['verbose'],
                debug = self.options['debug']
            )
            vlc.start()

class VideoTwisterOverlay(VideoTwisterBase):

    vlm_template = os.path.join(os.path.dirname(__file__), 'overlay_videos.vlm.tpl')

    def mungle_options(self):
        """Convert some variables to their proper types"""
        self.options['angle'] = int(self.options['angle'])
        self.options['segfaults'] = int(self.options['segfaults'])
        self.options['timeout'] = float(self.options['timeout'])
        self.options['width'] = int(self.options['width'])
        self.options['height'] = int(self.options['height'])

    def start(self):
        """Select VLM template for doing overlay stuff and run VLC."""
        self.automask()
        self.expandvlm()
        self.run_vlc_with_vlm(self.vlm_template)

    def automask(self):
        """
        Automatically generate a mask image for alpha compositing
        using given height, width and angle.

        TODO: Don't limit to rectangle masks only.
        """
        # grok overlay size from media itself
        if not self.options['width'] or not self.options['height']:
            overlay_info = VideoInfo(self.options['overlay'])
            self.options['width'], self.options['height'] = overlay_info.size

        # generate alpha mask image
        if not self.options['maskfile']:
            mask_size = (self.options['width'], self.options['height'])
            self.alphamask = AlphaMask(mask_size)
            self.alphamask.rectangle()
            self.alphamask.rotate(self.options['angle'])
            self.options['maskfile'] = self.alphamask.save(delete = not self.options['debug'])

    def expandvlm(self):
        """Compute some additional options to be passed to VLM template.

        Here's all the comfort:
            - auto generate alpha mask image
            - detect background (still image vs. video)

        """

        # real size of alpha mask image
        maskwidth_real, maskheight_real = self.mask_size
        masksize_real = ''
        masksize_real += 'width=' + str(maskwidth_real) + ','
        masksize_real += 'height=' + str(maskheight_real) + ','
        self.options['masksize_real'] = masksize_real

        # input channel (still image vs. video)
        background = self.options['background']
        if BackgroundType.byfilename(background) == BackgroundType.IMAGE:
            overlay_info = VideoInfo(self.options['overlay'])
            self.options['overlay_duration'] = overlay_info.duration * 1000
            input_channel = """
            # input: still image
            setup background input fake://
            setup background option fake-file="${background}"
            setup background option fake-duration=${overlay_duration}
            """
        else:
            input_channel = """
            # input: video
            setup background input "${background}"
            """
        self.options['input_channel'] = input_channel

        # whether to display the result in vlc
        self.options['display'] = self.options['watch'] and ',dst=display' or ''

    @property
    def mask_size(self):
        """Compute width and height of alphamask image.

        Returns:
            (width, height) -- image size as tuple

        """
        image = Image.open(self.options['maskfile'])
        return image.size


class BackgroundType(object):

    VIDEO = 1
    IMAGE = 2

    @classmethod
    def byfilename(self, filename):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.tif') or filename.endswith('.gif'):
            return self.IMAGE
        else:
            return self.VIDEO


def setup_logging():
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(name)-18s: %(levelname)-8s: %(message)s'))
    logger = logging.getLogger()
    logger.addHandler(console)
    logger.setLevel(logging.INFO)

def media_info(label, mediafile):
    print >>sys.stderr, "Media information (%s):" % label
    if BackgroundType.byfilename(mediafile) == BackgroundType.VIDEO:
        print >>sys.stderr, VideoInfo(mediafile).raw
        print >>sys.stderr
    elif BackgroundType.byfilename(mediafile) == BackgroundType.IMAGE:
        im = Image.open(mediafile)
        print >>sys.stderr, "File: %s" % mediafile
        print >>sys.stderr, "Format: %s" % im.format
        print >>sys.stderr, "Size: %dx%d" % im.size
        print >>sys.stderr, "Mode: %s" % im.mode
        print >>sys.stderr
        #if verbose:
        #    print im.info, im.tile,
    else:
        print >>sys.stderr, 'No media information'
        print >>sys.stderr


@opterate
def main(output, background, overlay,
        vlc=None,
        angle=0, position_x=0, position_y=0,
        maskfile=None, width=0, height=0,
        watch=False, segfaults=20, timeout=120, verbose=False, debug=False):
    """
    Overlay videos with alpha compositing and rotation using VLM from VLC.
    
    @param vlc -V --vlc path to vlc executable
    @param position_x -x --position-x x-position of the overlay (default: 0)
    @param position_y -y --position-y y-position of the overlay (default: 0)
    @param width -W --width width of the overlay (default: original size)
    @param height -H --height height of the overlay (default: original size)
    @param angle -a --angle which angle to rotate the overlay (default: 0)
    @param maskfile -m --mask overlay alpha mask image (optional)
    @param watch -w --watch whether to display the result in vlc (default: false)
    @param segfaults -s --segfaults how many segfaults to compensate for (default: 20)
    @param timeout -t --timeout when to timeout and kill VLC (default: 120s)
    @param verbose -v --verbose Use this if something goes wrong: a) doesn't suppress stdout and stderr of vlc b) sends '--verbose=2' to vlc c) doesn't send '--quiet' to vlc
    @param debug -d --debug Use this if something goes wrong: a) log vlc command (even in non-verbose mode) b) keep temporary files (vlm, vlc log, mask)
    """

    setup_logging()
    if verbose:
        logger.setLevel(logging.DEBUG)
    logger.info("zt.vlc.twister starting")
    options = locals()
    options.update({'output': output, 'background': background, 'overlay': overlay})

    if verbose or debug:
        media_info('background', options['background'])
        media_info('overlay', options['overlay'])

    twister = VideoTwisterOverlay(**options)
    twister.start()

if __name__ == '__main__':
    main()
