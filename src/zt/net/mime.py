#!/usr/bin/env python

"""Builds a multipart MIME message."""
# http://docs.python.org/library/email-examples.html

import os
import sys
import email
# For guessing MIME type based on file name extension
import mimetypes

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_message_multipart(entries):

    #outer = MIMEMultipart()
    outer = MIMEMultipart('form-data')

    for entry in entries:

        if 'file' in entry:
            name = entry['name']
            path = entry['file']
            if not os.path.isfile(path):
                continue
            msg = get_message_file(name, path)

        else:
            name = entry['name']
            value = entry['value']
            msg = get_message_variable(name, value)

        # Set the filename parameter
        del msg['MIME-Version']
        outer.attach(msg)

    #print dir(outer)

    del outer['MIME-Version']
    content_type = outer['Content-Type']

    composed = outer.as_string()
    #print "composed:\n", composed

    replstr = ''
    for sep in ['\n\t', ' ']:
        replstr = 'Content-Type: %s;%sboundary="%s"' % \
            (content_type, sep, outer.get_boundary())
        #print "replstr:", replstr
        composed = composed.replace(replstr, '')

    content_type = replstr
    composed = composed.lstrip()
    return content_type.split(' ', 1)[1], composed


def get_message_variable(name, value):
    msg = MIMEBase()
    msg.set_payload(value)
    msg.add_header('Content-Disposition', 'form-data', name=name)
    return msg


def get_message_file(name, path):
    # Guess the content type based on the file's extension.  Encoding
    # will be ignored, although we should check for simple things like
    # gzip'd or compressed files.
    ctype, encoding = mimetypes.guess_type(path)
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so
        # use a generic bag-of-bits type.
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        fp = open(path)
        # Note: we should handle calculating the charset
        msg = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'image':
        fp = open(path, 'rb')
        msg = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == 'audio':
        fp = open(path, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(path, 'rb')
        msg = MIMEBase(maintype, subtype)
        msg.set_payload(fp.read())
        fp.close()
        # Encode the payload using Base64
        encoders.encode_base64(msg)
    filename = os.path.basename(path)
    msg.add_header('Content-Disposition', 'attachment',
        name=name, filename=filename)
    return msg


class MIMEBase(email.message.Message):
    """Base class for MIME specializations."""

    def __init__(self, _maintype=None, _subtype=None, **_params):
        """This constructor adds a Content-Type: and a MIME-Version: header.

        The Content-Type: header is taken from the _maintype and _subtype
        arguments.  Additional parameters for this header are taken from the
        keyword arguments.
        """
        email.message.Message.__init__(self)
        if _maintype and _subtype:
            ctype = '%s/%s' % (_maintype, _subtype)
            self.add_header('Content-Type', ctype, **_params)
        #self['MIME-Version'] = '1.0'


def monkeypatch():
    email.mime.base.MIMEBase = MIMEBase
monkeypatch()


if __name__ == '__main__':
    main()
