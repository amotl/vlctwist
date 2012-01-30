========
vlctwist
========


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

    venv .venv
    . .venv/bin/activate

Install prerequisites::

    pip install -r requirements.txt
    python setup.py develop

Show help::

    vlctwist --help

Run daemon::

    vlctwistd

Run::

    ./vlctwist_example.sh
