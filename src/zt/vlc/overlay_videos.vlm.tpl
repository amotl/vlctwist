# Overlay videos with alpha compositing and rotation on top of VLC.
# Copyright 2012 Andreas Motl
# Licensed under the Apache License, Version 2.0 (the "License")


# ---------
#  overlay
# ---------

new overlay broadcast

setup overlay input ${overlay}

setup overlay output #transcode{vcodec=mp4v,vb=1500,scale=1,vfilter=rotate{angle=${angle}}}:duplicate{dst=mosaic-bridge{id=1,x=${position_x},y=${position_y},${masksize_real}chroma=YUVA,vfilter=alphamask{mask=${maskfile}}},select=video}

setup overlay enabled


# ------------
#  background
# ------------

new background broadcast

# input channel
${input_channel}

# Keep aspect ratio
setup background option mosaic-keep-aspect-ratio

# Keep original size
setup background option mosaic-keep-picture

setup background output #transcode{vcodec=mp4v,vb=4096,sfilter="mosaic"}:bridge-in:duplicate{dst=standard{access=file,mux=ps,dst="${output}"}${display}}

setup background enabled


# ----------
#  kick off
# ----------
control overlay play
control background play
