======================
zt.vlc api information
======================

.. contents::
    :depth: 2
    :local:


Valid request
-------------

::

    POST /twist/v1/mosaic HTTP/1.0
    content-type: multipart/form-data; boundary="===============0397538362560721606=="
    content-length: 27902144

    --===============0397538362560721606==
    Content-Disposition: form-data; name="output"

    /tmp/vlctwist.mpg
    --===============0397538362560721606==
    Content-Type: image/png
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; name="background";
     filename="surgical mask.png"

    iVBORw0KGgoAAAANSUhEUgAAAbUAAAHrCAAAAABtRVyGAAACfmlDQ1BJQ0MgUHJvZmlsZQAAeJyN
    kbtPFFEUxn8zYmwIGqOEUN2SGJaMj0Ls1gWWV9Z1WSJLTHScvbt72dmZ8c7sKoSKxsYIlbGwMeEP
    oLSgsCCh0WBC0L/AAh8J0YTSWMwKI/g61bnn3PN93/kOdKzZQeCaAhpepLOFdGmmNCtOvcWki04A
    [...]
    --===============0397538362560721606==
    Content-Type: video/quicktime
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; name="overlay"; filename="Fish.mov"

    JyT0qe3u7q2x9nmaP6VX02fzYwkgznvVuS3KScdK+zyHPaOZ0lbRo+JzfK6mAm23oUpfNlmaWVi7
    E8k0KmOtXPJOc0jQHHSvoIq8tjxfaplUrzxRtIBqwIiD0pfLznHWtVTk9w5ysAECxR8AdcU7bhec
    1b+zxhd4IAqhqF1HbWruzAADiv5PlVdepfqz+uIpYKhyS6HNeI9disLd4ojmQ8V5bdTy3MzSyNnN
    [...]
    --===============0397538362560721606==
    Content-Disposition: form-data; name="vlc"


    --===============0397538362560721606==
    Content-Disposition: form-data; name="angle"

    33
    --===============0397538362560721606==
    Content-Disposition: form-data; name="position_x"

    50
    --===============0397538362560721606==
    Content-Disposition: form-data; name="position_y"

    50
    --===============0397538362560721606==
    Content-Disposition: form-data; name="width"

    320
    --===============0397538362560721606==
    Content-Disposition: form-data; name="height"

    240
    --===============0397538362560721606==
    Content-Disposition: form-data; name="watch"

    True
    --===============0397538362560721606==
    Content-Disposition: form-data; name="segfaults"

    20
    --===============0397538362560721606==
    Content-Disposition: form-data; name="timeout"

    120
    --===============0397538362560721606==
    Content-Disposition: form-data; name="verbose"

    False
    --===============0397538362560721606==
    Content-Disposition: form-data; name="debug"

    False
    --===============0397538362560721606==
    Content-Disposition: form-data; name="remote"


    --===============0397538362560721606==--


Valid response
--------------
::

    HTTP/1.0 200 OK
    Date: Mon, 30 Jan 2012 17:26:00 GMT
    Server: WSGIServer/0.1 Python/2.6.6
    Vary: Accept
    Content-Length: 6729299
    Content-Disposition: attachment; name="output"; filename="vlctwist.mpg"
    Content-Type: video/mpeg
    Content-MD5: 0876f67133121082e48630cc4b114a49

    ....].m.................!....................k|M<....y...
    7g[...g[.................... ........=.c....Lavc53.5.0...
    [...]


Failed responses
----------------
::

    HTTP/1.0 500 Internal Server Error
    Date: Mon, 30 Jan 2012 11:39:17 GMT
    Server: WSGIServer/0.1 Python/2.6.6
    Vary: Accept
    Content-Length: 69
    Content-Type: text/xml; charset=UTF-8
    Content-MD5: 813fc86ab8c63740b74bec24e9982901

    <response><error>global name 'Hotzenplotz' is not defined</error></response>


::

    HTTP/1.0 500 Dude, this is whack!
    Date: Mon, 30 Jan 2012 17:34:04 GMT
    Server: WSGIServer/0.1 Python/2.6.6
    Content-Type: text/plain
    Content-Length: 59

    A server error occurred.  Please contact the administrator.

::

    zt.net.webcommand.client: ERROR   : Got invalid response (500 Dude, this is whack!), length="59", error="A server error occurred.  Please contact the administrator."
