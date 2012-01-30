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

import logging
from PIL import Image, ImageDraw
from tempfile import NamedTemporaryFile


class AlphaMask(object):
    """
    Generate a mask image for alpha compositing
    using given height, width and angle.

    TODO: Don't limit to rectangle masks only.
    """

    logger = logging.getLogger(__name__)

    def __init__(self, size, mode='RGBA'):
        """Create AlphaMask object, initialize image container"""
        self.logger.info('Create alpha mask image with size %s' % str(size))
        self.image = Image.new(mode, size)
        self.maskfile = None

    def rectangle(self, bbox=None):
        """
        Draw rectangle (default: full size)
        and put it on alpha channel of image.

        """
        if not bbox:
            bbox = (0, 0, self.image.size[0], self.image.size[1])
        mask = Image.new('L', self.image.size, color=0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle(bbox, fill=255)
        self.image.putalpha(mask)

    def rotate(self, angle, expand=True):
        """Rotate image by given angle"""
        self.image = self.image.rotate(angle, expand=expand)

    def save(self, delete=True):
        """Save image in PNG format to temporary file"""
        self.maskfile = NamedTemporaryFile(suffix='.png', delete=delete)
        name = self.maskfile.name
        self.image.save(name, 'png')
        self.logger.info('Saved alpha mask image with size %s to %s'
            % (str(self.image.size), name))
        return name


def main():
    """
    Example usage of AlphaMask:

    Input:
    - size: 320x240
    - action: draw rectangle in full size
    - action: rotate by 30 degrees, expanding the image size

    Output:
    - file: png image with rotated rectangle in alpha channel
    - size: 398x368

    """
    m = AlphaMask((320, 240))
    m.rectangle()
    m.rotate(30)
    print "Alpha compositing mask image:", m.save(delete=False)

if __name__ == '__main__':
    main()
