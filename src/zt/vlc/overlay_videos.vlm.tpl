# overlay
new overlay broadcast
setup overlay input ${overlay}
# works, but alphamask won't be fine due to missing "chroma=YUVA"

setup overlay output #transcode{vcodec=mp4v,vb=1500,scale=1,vfilter=rotate{angle=${angle}}}:duplicate{dst=mosaic-bridge{id=1,${masksize}vfilter=alphamask{mask=${maskfile}}},select=video}

# crashes arbitrarily/often
#setup overlay output #transcode{vcodec=mp4v,vb=1500,scale=1,vfilter=rotate{angle=${angle}}}:duplicate{dst=mosaic-bridge{id=1,${masksize}chroma=YUVA,vfilter=alphamask{mask="${maskfile}"}},select=video}
setup overlay enabled

# background
new background broadcast
setup background input ${background}
#setup background output #transcode{vcodec=mp4v,vb=4096,sfilter="mosaic"}:bridge-in:standard{access=file,mux=ps,dst="${output}"}${display}

setup background output #transcode{vcodec=mp4v,vb=4096,sfilter="mosaic"}:bridge-in:duplicate{dst=standard{access=file,mux=ps,dst="${output}"},dst=display}

#setup background output #transcode{vcodec=mp4v,vb=4096,sfilter="mosaic"}:bridge-in:display
setup background enabled

# kick off
control overlay play
control background play

#shutdown
