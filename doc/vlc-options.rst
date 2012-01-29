VLC::

    #cmd = [self.options['vlc'], '-I', 'dummy', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    #cmd = [self.options['vlc'], '-I', 'telnet', '--telnet-password', 'test', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    #cmd = [self.options['vlc'], '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    #cmd = [self.options['vlc'], '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], 'vlc://pause:2', 'vlc://quit']
    #cmd = [self.options['vlc'], '-I', 'macosx', '-I', 'telnet', '--telnet-password', 'test', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    # 'vlc://quit'

    #cmd = [self.options['vlc'], '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], 'vlc://quit']

    # If you want to have both the "normal" interface and the HTTP interface, use vlc --extraintf http.
    #cmd = [self.options['vlc'], '--extraintf', 'telnet', '--telnet-password', 'test', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]

    # http://mailman.videolan.org/pipermail/vlc-devel/2011-March/079232.html
    #-I rc --lua-config "rc={host='telnet://localhost:4212'}"
    #cmd = [self.options['vlc'], '--extraintf', 'rc', '--lua-config', "rc={host='telnet://localhost:4212'}", '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    #cmd = [self.options['vlc'], '-I', 'rc', '--lua-config', "rc={host='telnet://localhost:4212'}", '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    #cmd = [self.options['vlc'], '-I', 'rc', '--lua-config', "rc={*console}", '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    #cmd = [self.options['vlc'], '-I', 'dummy', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], self.options['overlay'], 'vlc://quit']
    #cmd = [self.options['vlc'], '-I', 'dummy', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], 'vlc://quit']
    #cmd = [self.options['vlc'], '-I', 'dummy', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]

    #cmd = [self.options['vlc'], '--play-and-exit', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], 'vlc://quit']
    #cmd = [self.options['vlc'], self.options['overlay'], 'vlc://quit', '-I', 'dummy', '--play-and-exit', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose']]
    #cmd = [self.options['vlc'], '-I', 'dummy', '--play-and-exit', '--no-interact', '--vlm-conf', vlmfile.name, '--mosaic-keep-picture', self.options['verbose'], self.options['overlay'], 'vlc://quit']


VLM::

    #setup background output #transcode{vcodec=mp4v,vb=4096,sfilter="mosaic"}:bridge-in:display
    #setup background output #transcode{vcodec=mp4v,vb=4096,sfilter="mosaic"}:bridge-in:standard{access=file,mux=ps,dst="${output}"}
    #setup background output #transcode{vcodec=mp4v,vb=4096,sfilter="mosaic"}:bridge-in:duplicate{dst=standard{access=file,mux=ps,dst="${output}"},dst=display}


Common::

    --play-and-exit
    --no-media-library
    --no-sout-all
    --no-sout-video
    --no-sout-audio
    --no-sout-keep
    --no-sout-display
    --no-sub-autodetect-file
    --no-autoscale
    --video-on-top
    --no-drop-late-frames
    --no-skip-frames
    --no-sout-transcode-hurry-up
