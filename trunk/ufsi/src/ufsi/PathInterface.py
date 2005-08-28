"""

TODO: move this to the class docstring.

The PathInterface class specifies the methods required on all Path
objects. All Path implementations must implement them and adhere to
their specifications.

A Path object provides an object oriented interface to path related
functions that are performable on a path.

Path object constraints and conditions:
 * All Path objects are immutable.
 * If authentication is required to execute a specified method, but it
   hasn't been provided (see: setAuthentication()) an
   AuthenticationError should be thrown.

TODO: these two points contradict each other...

Definitions:
*Authentication object*
  an instance (child) of ufsi.AuthentictionInterface

*Dir object*
  an instance (child) of ufsi.DirInterface

*File object*
  an instance (child) of ufsi.FileInterface

*Native path*
  a path that is handled by Python's ``os`` module and therefore by
  the underlying C functions.

path
  a string. Eg '/usr/bin/python'

*Path object*
  an instance (child) of ufsi.PathInterface


"""


class PathInterface:
    """
    TODO: finish. Look at FileInterface and DirInterface for an example.
    """

    def __init__(self,path):
        """
        Creates a Path object. This is the only place where it is
        acceptable to write to a Path object's instance variables.

        """
        raise NotImplementedError


    def __str__(self):
        """
        Returns a string representation of the Path.

        Preconditions
         * None

        Postconditions
         * A string that is interpreted  to refer to the same location
           as  the path  string used  to  create this  Path object  is
           returned. Ie, it  may not be the exact  same string if, for
           example, the operating  system understands both the forward
           slash and back slash characters as separator characters.

        """
        raise NotImplementedError


    def split(self):
        """
        Splits this path into its various parts and returns the parts
        in a dict. Common parts are:
         * protocol - HTTP, FTP, NativePath (for paths without a
           protocol given), etc... Special cases are:
            + A windows drive based path should have a protocol type
              of 'NativeWindowsDrivePath'.
            + A windows UNC based path should have a protocol type of
              'NativeWindowsUNCPath'.
         * host - the name (or ip address) of the computer on which
           the file system resides.
         * port - the port number used to connect to the file system,
           or undefined if the default port number should be used.
         * dirs - a list of directory names, or an empty list if no
           directories were given.
         * fileName - anything after the last separator character.
         * fileBase - the part of the filename before the last period
           character.
         * fileExt - the part of the filename after the last period
           character.

        Note: Since Path objects are immutable, this method should be
        optimised to cache the result for subsequent calls.

        Preconditions:
         * None

        Postconditions:
         * A dict is returned which must contain any of the above
           defined parts if they are applicable, and also other parts
           that are specific to a certain file system type. For
           example, a windows path should also define 'drive' if the
           path contains a drive letter specification.
         * The only required parts are protocol, dirs, fileName and fileBase
           since a path should always be able to define these things
           even if it happens to be an empty dir list and a ''
           fileBase. TODO: a fileBase may not always be present: FTPUrl
           
        """
        raise NotImplementedError

    def join(self,other):
        """
        Joins a path on to the end of this path. Acceptable values for
        ``other`` are a string or a Path object. If ``other`` is an
        absolute path it alone is the return value.

        Preconditions:
         * ``other`` is a string or a Path object

        Postconditions:
         * If ``other`` is an absolute path, the return value is a
           Path object that represents the path defined by ``other``.
         * If ``other`` is a relative path, the return value is a Path
           object that represents the result of appending ``other``
           onto the end of the path that this Path object represents.

        """
        raise NotImplementedError


    def isAbsolute(self):
        """
        Returns True if this path is an absolute path. This means that
        the path is not relative to any current working
        directory. Therefore, all paths that involve a host must be
        absolute. Windows paths that start with a drive letter are
        absolute and Native paths that start with a separator
        character are absolute.

        Preconditions:
         * None

        Postconditions:
         * Returns True if the path is absolute, False otherwise.

        """
        raise NotImplementedError


    def getSeparator(self):
        """
        Returns the separator string used to separate dirs.

        Preconditions:
         * None

        Postconditions:
         * Returns a string of at least one character that occurs
           between each directory in the path.

        """
        raise NotImplementedError


    def setAuthentication(self,auth):
        """
        Sets the authentication object for this Path object and any
        derived objects that would require authentication information.

        Preconditions:
         * None

        Postconditions:
         * Any methods that might require authentication now have an
           authorisation object that can provide authentication
           information to the file system being accessed.

        """
        raise NotImplementedError

    def getAuthentication(self):
        """
        Returns the previously set authentication object.

        Preconditions:
         * None

        Postconditions:
         * Returns an authentication object, or ``None`` if an
           authentication object hasn't been set yet.
        """
        raise NotImplementedError
        

    def isFile(self):
        """
        Returns a boolean to indicate whether the path refers to a
        file on the file system. The return value will only be True if
        the path exists on the file system and it refers to a
        file. Symbolic links should be followed.

        Preconditions:
         * None

        Postconditions:
         * Returns True if the path refers to an existing item on
           the file system and that item is a file.
         * Returns False if either of the above conditions are not
           met.
        
        """
        raise NotImplementedError

    def isDir(self):
        """
        Returns a boolean to indicate whether the path refers to a
        dir on the file system. The return value will only be True if
        the path exists on the file system and it refers to a
        directory. Symbolic links should be followed.

        Preconditions:
         * None

        Postconditions:
         * Returns True if the path refers to an existing item on
           the file system and that item is a dir.
         * Returns False if either of the above conditions are not
           met.
        
        """
        raise NotImplementedError
        
    def isSymlink(self):
        """
        Returns a boolean to indicate whether the path refers to a
        symlink on the file system. The return value will only be True
        if the path exists on the file system and it refers to a
        symlink. Naturally, symlinks should be followed up until the
        actual filename.

        Preconditions:
         * None

        Postconditions:
         * Returns True if the path refers to an existing item on the
           file system and that item is a symlink.
         * Returns False if either of the above conditions are not
           met.
        
        """
        # TODO: should it actually just be called link? More generic.
        raise NotImplementedError
        

    def getFile(self):
        """
        Returns a File object that will access the file located at
        this path. No check is performed to determine whether it
        actually exists; exceptions/errors will occur later when using
        the File object.

        Preconditions:
         * None

        Postconditions:
         * A File object is returned.

        """
        raise NotImplementedError

    def getDir(self):
        """
        Returns a Dir object that will access the dir located at this
        path. No check is performed to determine whether it actually
        exists; exceptions/errors will occur later when using the Dir
        object.
        
        Preconditions:
         * None

        Postconditions:
         * A Dir object is returned.

        """
        raise NotImplementedError
        
    def getSymlinkPath(self):
        """
        Returns a Path object that is the path to the item referred to
        by the symlink. This path should be the same path as the
        symlink and must not be joined onto this path. 

        Preconditions:
         * self.isSymlink()==True

        Postconditions:
         * Result is a Path object that refers to the item that the
           symlinks points to. If this Path object has been given an
           Authentication object and the symlink path is on the same
           file system, the resulting Path object is also given this
           Authentication object.
        
        """
        raise NotImplementedError


    """
    TODO: Additional methods to be added later:
     * getFileName
     * getFileBase
     * getDirsList
     * getDirsString
     * ...

     * getParentDirPath
     * getNormalisedPath

     * isRelative
    """
