"""
Handles the creation of native path implementations of
``ufsi.PathInterface``.

"""

from NativeUnixPath import NativeUnixPath
from NativeWindowsPath import NativeWindowsPath

import os


def NativePath(path):
    """
    Checks the type of the current operating system and creates the
    appropriate native implementation of a Path object.

    If an empty string is passed as the path, the cwd is used.
    """
    if path=='':
        path=os.getcwd()

    if os.name=='nt':
        # TODO: include check for unc style path later
        return NativeWindowsPath(path)
    else:
        return NativeUnixPath(path)

