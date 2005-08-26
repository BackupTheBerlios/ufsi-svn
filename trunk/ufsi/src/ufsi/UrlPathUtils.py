"""
Common utility functions for handling UrlPaths. A UrlPath is defined
in RFC1738 as being anything after:

  protocol://<user>:<password>@<host>:<port>/


"""


import ufsi

import re

# TODO: include a method to take into account ;typeParams, ?queryParams
# and #fragments


def splitHeirarchicalUrlPath(urlPath):
    """
    Splits a url path of the type:
    
      [/]{<dir1>/}<fileBase>[.<fileExt>]

    * dirs - must be present, but may be an empty list
    * fileBase - None if no slash after the host
    * fileExt - None if no period after the fileBase

    """
    d={}
    if urlPath is not None:
        dirs=urlPath.split('/')
        fileName=dirs.pop()

        if '.' in fileName:
            (fileBase,fileExt)=fileName.rsplit('.')
        else:
            fileBase=fileName
            fileExt=None
    
    else:
        dirs=[]
        fileBase=None
        fileExt=None

    d['dirs']=dirs
    d['fileBase']=fileBase
    d['fileExt']=fileExt

    return d


