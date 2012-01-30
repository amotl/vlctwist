##############################################################################
#
# Copyright 2012 Andreas Motl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
##############################################################################

import os
import sys
import inspect
import logging
from tempfile import NamedTemporaryFile
from pprint import pprint, pformat
# http://packages.python.org/WsgiService/tutorial.html
from wsgiservice import get_app, mount, Resource
from wsgiservice import raise_201, raise_404, raise_500
from wsgiref.simple_server import make_server
import cgi
import base64
import mimetypes
from opterator import opterate
from zt.util.log import setup_logging


logger = logging.getLogger(__name__)

bridge_func = None
schema = {'all': [], 'args': [], 'options': []}


@mount('/twist/v1/mosaic')
class WebTwister(Resource):

    NOT_FOUND = (KeyError,)

    """
    qt		video/quicktime
    avi 	video/x-msvideo
    m4v 	video/x-m4v
    mov 	video/quicktime
    mp4 	video/mp4
    mpe 	video/mpeg
    mpeg 	video/mpeg
    mpg 	video/mpeg
    """
    def POST(self):
        """Convert video"""

        results = self.dispatch()

        if not results:
            raise_404(self, 'No results!')

        result = results[0]

        # will get **really** big: contains binary payloads
        # TODO: strip this payload to show it for informational purposes
        #logger.info('dispatching control data:\n%s' % pformat(result))

        self.type = result['content_type']
        self.charset = None
        self.response.body = result['body']
        #self.response.body_raw = retval
        self.response.headers.update(result['headers'])

        #print "response headers:",
        #pprint(self.response.headers)

        #raise_201(self, 5)
        #return "Hello"

    def mungle_option_item(self, item):
        logger.debug("mungle_option_item-before: %s" % item)
        item.exists = item.name in self.request.POST
        item.value = self.request.POST.get(item.name, item.default)

        if isinstance(item.value, cgi.FieldStorage):
            fieldstorage = item.value
            item.filename_submitted = \
                os.path.basename(fieldstorage.filename).encode('utf8')
            fileName, fileExtension = os.path.splitext(fieldstorage.filename)
            inputfile = NamedTemporaryFile(prefix=fileName, \
                suffix=fileExtension, delete=False)
            payload = fieldstorage.file.read()
            tenc = fieldstorage.headers.get('Content-Transfer-Encoding')
            if tenc == 'base64':
                payload = base64.decodestring(payload)
            inputfile.file.write(payload)
            inputfile.file.flush()
            item.value = inputfile.name

        if item.isfile and item.isretval:
            item.filename_submitted = \
                os.path.basename(item.value).encode('utf8')
            fileName, fileExtension = os.path.splitext(item.filename_submitted)
            outputfile = NamedTemporaryFile(prefix=fileName, \
                suffix=fileExtension, delete=False)
            item.value = outputfile.name

        if item.convert is bool:
            item.value = \
                item.convert(item.value.lower() == 'true' and True or False)
        else:
            item.value = item.convert(item.value)

        logger.debug("mungle_option_item-after : %s" % item)

    def dispatch(self):

        import zt.net.webcommand.server
        schema = zt.net.webcommand.server.schema
        bridge_func = zt.net.webcommand.server.bridge_func

        args = []
        kwargs = {}

        for i, item in enumerate(schema['args']):
            self.mungle_option_item(item)
            if not item.exists:
                raise KeyError('Argument "%s" is missing (position #%s)' % \
                    (item.name, i))
            args.append(item.value)

        for item in schema['options']:
            self.mungle_option_item(item)
            if item.exists:
                kwargs[item.name] = item.value

        target_parts = [bridge_func.__module__, bridge_func.func_name]
        target_label = '.'.join(target_parts)
        logger.info("Dispatching request to %s" % target_label)
        bridge_func(*args, **kwargs)

        results = []
        for i, item in enumerate(schema['all']):
            if item.isretval:
                result = self.item_to_result(item)
                results.append(result)

        return results

    def item_to_result(self, item):
        if item.isfile:
            filename = os.path.basename(item.value)
            ctype, encoding = mimetypes.guess_type(filename)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded
                # (compressed), so use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            payload = file(item.value, 'rb').read()
            payload_length = len(payload)
            logger.info(('Read result file "%s"", length="%s", ' + \
                'content-type-guess="%s"') % \
                (item.value, payload_length, ctype))
            if payload_length <= 1000:
                msg = 'We have a backend problem, apologies! Please try again.'
                logger.error(msg)
                raise_500(self, msg)
            result = {
                'content_type': ctype,
                'body': payload,
                'headers': {
                    'Content-Disposition':
                        'attachment; name="%s"; filename="%s"' % \
                            (item.name, item.filename_submitted),
                },
            }
        else:
            result = {
                'content_type': 'text/plain',
                'body': item.value,
                'headers': {},
            }
        return result


class OptionItem(dict):

    def __init__(self, data=None):
        data = data or {}
        self.__dict__.update(data)

    def __getattr__(self, attr):
        return self[attr]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.__dict__)


def webify(func):

    webify.filenames = webify.filenames or []

    global bridge_func
    global schema

    bridge_func = func

    argnames, varargs, varkw, defaults = inspect.getargspec(func)

    if defaults:
        positional_params = argnames[:-1 * len(defaults)]
        kw_params = argnames[-1 * len(defaults):]
    else:
        positional_params = argnames
        kw_params = []

    #print "positional_params:", positional_params
    #print "kw_params:", kw_params

    def get_item(name, convert, default, ispositional=False):
        isfile = isretval = False
        if name in webify.filenames:
            isfile = True
        if name == webify.retval:
            isretval = True
        item = OptionItem(locals())
        schema['all'].append(item)
        return item

    for name in positional_params:
        item = get_item(name, str, '', ispositional=True)
        schema['args'].append(item)

    for name in kw_params:
        default = defaults[kw_params.index(name)]
        item = get_item(name, type(default), default)
        schema['options'].append(item)

    logger.debug("Reflected parameter schema:\n%s" % pformat(schema['all']))

    return func


@opterate
def main(port=8001, verbose=False):
    """
    Overlay videos with alpha compositing and rotation using VLM from VLC.

    @param port -p --port Port to listen on
    @param verbose -v --verbose More output

    """
    loglevel = verbose and logging.DEBUG or logging.INFO
    setup_logging(loglevel)
    logger.setLevel(loglevel)
    # TODO: make this configurable to decouple
    # zt.net.webcommand completely from zt.vlc
    __import__('zt.vlc.twister')
    logger.info("Starting web server on port 8001")
    #app = get_app(globals())
    app = get_app({'WebTwister': WebTwister})
    make_server('', int(port), app).serve_forever()

if __name__ == '__main__':
    main()
