# this is a namespace package
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    pass


def find_vlc():
    # FIXME: actually search for the executable,
    # maybe prefer ``cvlc`` instead of ``vlc``.
    return '/Applications/VLC.app/Contents/MacOS/VLC'
