
version = '0.1.0'

from setuptools import setup, find_packages
setup (
    name = 'zt.vlc',
    version = version,
    description = 'Overlay videos with alpha compositing and rotation using VLM from VLC',
    author = 'Andreas Motl',
    author_email = 'andreas.motl@ilo.de',
    url = 'https://github.com/amotl/vlctwist',
    license = 'License :: OSI Approved :: Apache Software License',
    
    packages = find_packages('src'),

    include_package_data = True,
    package_dir = {'': 'src'},
    namespace_packages = ['zt'],
    zip_safe = False,

    # TODO: http://cburgmer.posterous.com/pip-requirementstxt-and-setuppy
    extras_require = dict(
        test = [
        ]
    ),
    install_requires = [
        'setuptools>=0.6c9',
        'decorator==3.3.2',
        'PIL==1.1.7',
        'WsgiService==0.3',
    ],
    entry_points = {
        'console_scripts': [
            'vlctwist=zt.vlc.twister:main',
            'vlctwistd=zt.net.webcommand.server:main',
        ],
    },
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: WsgiService',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Multimedia :: Graphics :: Editors :: Raster-Based',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Multimedia :: Graphics :: Presentation',
        'Topic :: Multimedia :: Video :: Conversion',
    ],
)
