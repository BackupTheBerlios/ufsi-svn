"""

Handles any IP-based protocol's url (as defined in RFC1738):

  protocol://<user>:<password>@<host>:<port>/<url-path>

Note: RFC1738 refers to protocols such as HTTP, FTP, GOPHER as
schemes, whereas the ``ufsi`` module refers to them as protocols, due
to more common usage.

TODO: extend this to take into account ;typeParams, ?queryParams and
#fragments

"""


import ufsi

import re


class AbstractUrlPath(ufsi.PathInterface):
    def __init__(self,path):
        self._path=path
        self._auth=None


    def __str__(self):
        """
        Returns the path as a string.
        """
        return self._path


    def join(self,other):
        """
        other should be a string or a Path object, otherwise a
        TypeError will be thrown.

        TODO: fix having to go through ufsi.Path *if simplistic/possible*
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

                pathStr=self._path
                pathSep=self.getSeparator()
                if not pathStr.endswith(pathSep):
                    pathStr+=pathSep

                return ufsi.Path(pathStr+otherStr)

        else:
            raise TypeError("join method requires a string or a"+\
                            "ufsi.Path object")


    def split(self):
        """
        Splits a URL of the type:

          protocol://<user>:<password>@<host>:<port>/<url-path>

        into:

        * protocol - must be present
        * user - None if not given
        * password - None if not given, empty if user:@host
        * host - must be present
        * port - None if not given (ie. None if using the default
          port)
        * urlPath - the part of the path that comes after the
          host/port definition. It does not contain the initial '/'
          character. If no trailing '/' occurs after the host/port
          part urlPath will be None.


        Raises:

        * InvalidPathError when the URL doesn't match the regular
          expression. Generally this means that the URL is invalid but the
          regular expression may be erroneous in some cases.

        """
        urlRePat=r'(?P<protocol>[^:/]+)://'+\
               '((?P<user>[^:@/]+)(:(?P<password>[^:@/]+))?@)?'+\
               '(?P<host>[^/]+)(:(?P<port>[0-9]+))?'+\
               '(/(?P<urlPath>.*))?'
        

        urlRe=re.compile(urlRePat)
        mo=urlRe.match(pathStr)
        if mo is None:
            raise ufsi.InvalidPathError('"%s" is not a valid URL.'%pathStr)
        d=mo.groupdict()
        # upper and lower case protocols are considered the same
        # TODO: should we perform this transposition on creating the
        # Path object?
        d['protocol']=d['protocol'].lower()
        return d


    def getAuthorisation(self):
        """
        Returns the currently set Authorisation object or None if none
        have been set yet.
        """
        return self._auth

    def setAuthorisation(self,auth):
        """
        Sets the Authorisation object to use when performing
        requests.
        """
        self._auth=auth


