#!/bin/bash

export PYTHONPATH=`pwd`

case "$1" in
     --help)
           python zt/vlc/twister.py --help
           exit
           ;;
esac


# Usage: twister.py [options] output background overlay
python zt/vlc/twister.py \
    "/tmp/vlctwist.mpg" \
	"/System/Library/Compositions/Sunset.mov" \
    "/System/Library/Compositions/Fish.mov" \
	--position-x=50 --position-y=50 \
	--width=320 --height=240 \
    --angle=33 \
    --watch  # --debug   # --verbose


	# --mask="mask7.png"
    # --timeout=2
    # --segfaults=3

#"/System/Library/Compositions/Sunset.mov" \
#"/Library/Dictionaries/New Oxford American Dictionary.dictionary/Contents/Images/surgical mask.png" \
