import httplib
import urlparse


def posturl(url, content_type, message):
    urlparts = urlparse.urlsplit(url)
    return _posturl(urlparts[1], urlparts[2], content_type, message)


def _posturl(host, selector, content_type, request_body):
    """
    Sends HTTP POST and returns the server's response,
    which is a quadruple as of: (errcode, errmsg, headers, response_body)
    """
    h = httplib.HTTP(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(request_body)))
    h.endheaders()
    h.send(request_body)
    errcode, errmsg, headers = h.getreply()
    response_body = h.file.read()
    return errcode, errmsg, headers, response_body
