"""

Handles any IP-based protocol's url (as defined in RFC1738):

  protocol://<user>:<password>@<host>:<port>/<url-path>

Note: RFC1738 refers to protocols such as HTTP, FTP, GOPHER as
schemes, whereas the ``ufsi`` module refers to them as protocols, due
to more common usage.

Note: Although we call paths of this format UrlPaths (as in a URL
based path) we also call the content after the '/' after the host and
optional port a urlPath (as in the url's path part), as it is called
in RFC1738. Generally the case and context of the word's use should
make the meaning clear.

TODO: extend this to take into account ;typeParams, ?queryParams and
#fragments

"""


import ufsi

import re


class AbstractUrlPath(ufsi.PathInterface):
    """
    An abstract implementation of a URL based path. Defines the
    following methods:

    * __str__
    * join
    * split
    * getAuthentication
    * setAuthentication

    Defines the following attributes:

    * _path
    * _auth

    """

    
    def __init__(self,path):
        """
        Sets up common attributes of a UrlPath.
        """
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

        An implementing class should use this method to perform part
        of the splitting process but should also split the urlPath
        into more meaningful parts and append those parts to the
        returned dict.


        Raises:

        * InvalidPathError when the URL doesn't match the regular
          expression. Generally this means that the URL is invalid but
          the regular expression may be erroneous in some cases.

        """
        urlRePat=r'(?P<protocol>[^:/]+)://'+\
               '((?P<user>[^:@/]+)(:(?P<password>[^:@/]+))?@)?'+\
               '(?P<host>[^/]+)(:(?P<port>[0-9]+))?'+\
               '(/(?P<urlPath>.*))?'
        

        urlRe=re.compile(urlRePat)
        mo=urlRe.match(self._path)
        if mo is None:
            raise ufsi.InvalidPathError('"%s" is not a valid URL.'%self._path)
        d=mo.groupdict()
        # upper and lower case protocols are considered the same
        # TODO: should we perform this transposition on creating the
        # Path object?
        d['protocol']=d['protocol'].lower()
        return d


    def getAuthentication(self):
        """
        Returns the currently set Authentication object or None if
        none have been set yet.
        """
        return self._auth

    def setAuthentication(self,auth):
        """
        Sets the Authentication object to use when performing
        requests.
        """
        self._auth=auth


