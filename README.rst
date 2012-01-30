========
vlctwist
========

.. contents::
    :depth: 2
    :local:

About
-----
Overlay videos with `alpha compositing`_ and rotation_ using VLM_ from VLC_.

.. _alpha compositing: http://en.wikipedia.org/wiki/Alpha_compositing
.. _rotation: http://en.wikipedia.org/wiki/Rotation
.. _VLC: http://www.videolan.org/
.. _VLM: http://wiki.videolan.org/Documentation:Streaming_HowTo/VLM


Getting started
---------------

Create and activate isolated python environment::

    aptitude install python-virtualenv    # optional
    virtualenv --no-site-packages .venv
    . .venv/bin/activate

Install prerequisites::

    easy_install pip              # optional
    pip install -r requirements.txt
    python setup.py develop

Standalone / client::

    vlctwist --help
    ./vlctwist_example.sh

Daemon::

    vlctwistd --help
    vlctwistd


Issues
------

Debian::

    # The required version of setuptools (>=0.6c9) is not available
    easy_install -U setuptools


Ubuntu::

    # zt.graphics.alpha   : INFO    : Create alpha mask image with size (320, 240)
    # wsgiservice.resource: ERROR   : An exception occured while handling the request: encoder zip not available

    # 1. setup dependencies
    aptitude install libjpeg libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev

    # 2. Install PIL with Jpeg support on Ubuntu Oneiric 64bit
    # http://jj.isgeek.net/2011/09/install-pil-with-jpeg-support-on-ubuntu-oneiric-64bits/

    ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib
    ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib
    ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib
    pip install --upgrade PIL


Development
-----------

Code style checks::

    pip install pep8
    pep8 --repeat src/
