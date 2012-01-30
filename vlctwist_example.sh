#!/bin/bash

case "$1" in
     --help)
           vlctwist --help
           exit
           ;;
esac


# Usage: twister.py [options] output background overlay
vlctwist \
    "/tmp/vlctwist.mpg" \
	"/Library/Dictionaries/New Oxford American Dictionary.dictionary/Contents/Images/surgical mask.png" \
    "/System/Library/Compositions/Fish.mov" \
	--position-x=50 --position-y=50 \
	--width=320 --height=240 \
    --angle=33 \
    --watch	--remote="http://localhost:8001/twist/v1/mosaic"  # --debug   # --verbose


	# --mask="mask7.png"
    # --timeout=2
    # --segfaults=3

#"/System/Library/Compositions/Sunset.mov" \
#"/Library/Dictionaries/New Oxford American Dictionary.dictionary/Contents/Images/surgical mask.png" \
