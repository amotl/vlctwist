# this is a namespace package
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass


import os

vlc_locations = [
    '/usr/bin/vlc',
    '/Applications/VLC.app/Contents/MacOS/VLC',
]

def find_vlc():
    # FIXME: maybe prefer ``cvlc`` instead of ``vlc``.
    for vlc in vlc_locations:
        if os.path.isfile(vlc):
            return vlc
