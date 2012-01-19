#!/bin/bash

vlc=/Applications/VLC.app/Contents/MacOS/VLC

#$vlc -v --vlm-conf rotate_mask_overlay.vlm --mosaic-keep-picture
#$vlc -v --vlm-conf zt/vlc/overlay_videos.vlm --mosaic-keep-picture

python zt/vlc/twister.py "output2.mov" "/System/Library/Compositions/Sunset.mov" "/System/Library/Compositions/Fish.mov" --mask "mask.png" --watch --verbose
