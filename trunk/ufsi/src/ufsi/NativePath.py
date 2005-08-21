"""
Handles the creation of native path implementations of
``ufsi.PathInterface``.

"""

from NativeLinuxPath import NativeLinuxPath


def NativePath(path):
    """
    Checks the type of the current operating system and creates the
    appropriate native implementation of a Path object.
    """
    # TODO: insert check for os type
    return NativeLinuxPath(path)

