import os, sys
import logging
import inspect
from decorator import decorator
from tempfile import NamedTemporaryFile
from pprint import pprint, pformat
from zt.net.mime import get_message_multipart
from zt.net.http import posturl

from zt.util.log import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

def proxify(url_option = '', filenames = None, retval = None):
    
    filenames = filenames or []
    retval = retval or {}
    
    def inner(f, *args, **kwargs):
        argnames, varargs, varkw, defaults = inspect.getargspec(f)
        if defaults:
            positional_params = argnames[:-1*len(defaults)]
            kw_params = argnames[-1*len(defaults):]
        else:
            positional_params = argnames
            kw_params = []
        
        args = list(args)

        def get_value(name):
            index = argnames.index(name)
            value = args[index]
            return value

        def set_value(name, value):
            index = argnames.index(name)
            args[index] = value
        
        def reset_value(name):
            index = argnames.index(name)
            args[index] = defaults[index - len(positional_params)]
        
        url = get_value(url_option)
        if url:
            logger.info('Using remote video processor at "%s"' % url)

            reset_value(url_option)

            entries = []
            for name in argnames:
                value = get_value(name)
                if name in filenames:
                    entry = {'name': name, 'file': value}
                else:
                    entry = {'name': name, 'value': str(value)}
                entries.append(entry)

            logger.debug('Client will send options:\n%s' % pformat(entries))

            request_content_type, message = get_message_multipart(entries)
            errcode, errmsg, headers, payload = posturl(url, request_content_type, message)

            response_content_type = headers.get('content-type')
            if errcode == 200:
                exitcode = 0
                logger.info('Got valid response (%s %s), length="%s", content-type="%s"' % (errcode, errmsg, len(payload), response_content_type))
                output_file = get_value('output')
                with file(output_file, 'wb') as f:
                    f.write(payload)
                logger.info('Processing finished successfully, result="%s"' % output_file)
            else:
                exitcode = 1
                error_description = ''
                if 'text/' in response_content_type:
                    error_description = payload
                logger.error('Got invalid response (%s %s), error="%s", length="%s", content-type="%s"' % (errcode, errmsg, error_description, len(payload), response_content_type))
            
            def dummy():
                sys.exit(exitcode)
            return dummy
        else:
            return f(*args, **kwargs)
    
    return decorator(inner)
