"""
"""

import ufsi

import urllib2


def handleException(e,path):
    """
    Handles any exception that may be generated by this class.
    This class doesn't recover from an exception, it just raises
    an ufsi compliant exception.


    Postconditions:

    * An exception has been raised.

    TODO: move to HttpUtils.py

    """
    if isinstance(e,urllib2.HTTPError):
        if e.code==404:
            raise ufsi.PathNotFoundError(
                    'HTTP server returned 404 error whilst '
                    'trying to access url: "%s"'%path,e)
    else:
        # we don't know what it is so re-raise it
        raise e
