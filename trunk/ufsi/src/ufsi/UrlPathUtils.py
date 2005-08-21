"""

Handles a subclass of URLs - any url of the form (Adapted from RFC1738):

  protocol://[<user>:<password>@]<host>[:<port>]/<dir1>/../<dirN>/<fileName>

Note: RFC1738 refers to protocols such as HTTP, FTP, GOPHER as
schemes, whereas the ``ufsi`` module refers to them as protocols, due
to more common usage.

TODO: extend this to take into account ;typeParams, ?queryParams and
#fragments

"""


import ufsi
import re


# TODO: this is currently not used - we may not need it at all.
class AbstractUrlPath(ufsi.PathInterface):
    def __init__(self,path):
        # Abstract class
        raise NotImplementedError


def _join(pathStr,other):
    """
    pathStr must be a string.
    other should be a string or a Path object, otherwise a
    TypeError will be thrown.

    TODO: fix having to go through ufsi.Path *if simplistic*
    """
    if isinstance(other,basestring):
        other=ufsi.Path(other)

    if isinstance(other,ufsi.PathInterface):
        if other.isAbsolute():
            return other

        else:
            otherStr=str(other)
            otherSep=other.getSeparator()
            # remove any leading separator character on other
            while otherStr.startswith(otherSep):
                otherStr=otherStr[len(otherSep):]

            pathSep=self.getSeparator()
            if not pathStr.endswith(pathSep):
                pathStr+=pathSep

            return ufsi.Path(pathStr+otherStr)

    else:
        raise TypeError("join method requires a string or a"+\
                        "ufsi.Path object")


def _split(pathStr):
    """
    Splits a URL of the type:

      protocol://
        [<user>:<password>@]<host>[:<port>]/
        <dir1>/../<dirN>/<fileName>

    into:
    * protocol - must be present
    * user - None if not given
    * password - None if not given, empty if user:@host
    * host - must be present
    * port - None if not given (ie. None if using the default
      port)
    * dirs - must be present
    * fileBase - None if no slash after the host (TODO: fix def)
    * fileExt - None if no period after the fileBase

    TODO: later include typeParams, queryParams and fragments

    Raises:

    * InvalidPathError when the URL doesn't match the regular
      expression. Generally this means that the URL is invalid but the
      regular expression may be erroneous in some cases.

    """
    urlRePat=r'(?P<protocol>[^:/]+)://'+\
           '((?P<user>[^:@/]+)(:(?P<password>[^:@/]+))?@)?'+\
           '(?P<host>[^/]+)(:(?P<port>[0-9]+))?'+\
           '(/(?P<urlPath>[^;?#]*))?'
           #'(;(?P<typeParams>...

    urlRe=re.compile(urlRePat)
    mo=urlRe.match(pathStr)
    if mo is None:
        raise ufsi.InvalidPathError('"%s" is not a valid URL.'%pathStr)
    d=mo.groupdict()

    urlPath=d.get('urlPath')
    del d['urlPath']

    if urlPath is not None:
        dirs=urlPath.split('/')
        fileName=dirs.pop()

        if '.' in fileName:
            (fileBase,fileExt)=fileName.rsplit('.')
        else:
            fileBase=fileName
            fileExt=None
    
    else:
        # No trailing /
        dirs=[]
        fileBase=None
        fileExt=None

    d['dirs']=dirs
    d['fileBase']=fileBase
    d['fileExt']=fileExt

    return d


# TODO: remove this test code
if __name__=='__main__':
    p=r'http://www.google.com.au'
    print p
    s=_split(p)
    for k in (
            'protocol',
            'user',
            'password',
            'host',
            'port',
            'dirs',
            'fileBase',
            'fileExt'):
        print k+':'+(' '*(12-len(k)))+repr(s[k])
    
