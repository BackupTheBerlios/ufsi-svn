"""
A File object provides an object oriented interface to file related
functions that are performable on a file.

The FileInterface class specifies the methods required on all File
objects. All File implementations must implement them and adhere to
their specifications.

"""

class FileInterface:
    """
    The FileInterface class cannot be instantiated as it is really
    just an interface definition. Each method's docstring contains the
    specification for that method.
    
    """

    
    def __init__(self,path):
        """
        Creates an instance of the File implementation given a Path
        object.


        Preconditions:

        * path is an instance of PathInterface.


        Postconditions:

        * a File object is instantiated.

        """
        raise NotImplementedError


    def __str__(self):
        """
        Returns the path to this file (as a string, of course).


        Preconditions:

        * None


        Postconditions:

        * The path to the file that this File object works on is
          returned.

        """
        raise NotImplementedError


    def open(self,mode=None):
        """
        Opens the file with the given mode. Valid modes are:

        * r - (the default) reads the file.
        * w - writes to the file. Opening a file in this manner
          truncates it.
        * a - appends to the end of the file.

        Note: Not all file systems support all of the above modes. If
        a mode is not supported an UnsupportedOperationError should be
        raised when trying to use it.

        Additionally some mode modifiers are allowed:

        * b - specifies binary mode. The default mode is text
          based. Many file systems don't differenciate but some
          (eg. FTP) do
        * + - specifies open for update. This means that a file can be
          written to as well as read.? TODO: invesitgate this


        Preconditions:

        * If opening for read mode the file must exist.


        Postconditions:

        * The file is opened for reading or writing depending on the
          specified mode, or a UnsupportedOperationError has been
          rasied if the mode is not supported for that file system.
        
        """
        raise NotImplementedError


    def read(self,size=None):
        """
        Reads up to ``size`` bytes from the file. If ``size`` is None
        the file is read up to EOF. On encountering EOF immediately an
        empty string is returned.


        Preconditions:

        * The file is already open with a read mode.


        Postconditions:

        * Up to size bytes were read from the file. If EOF was
          encountered less bytes were read.

        """
        raise NotImplementedError

    def readLine(self):
        """
        Reads a single line from the file. Any end of line
        characters are left on. On encountering EOF immediately an
        empty string is returned.


        Preconditions:

        * The file is already open with a text read mode.


        Postconditions:

        * The next line of the file is read and returned.

        """
        raise NotImplementedError

    def readLines(self):
        """
        All remaining lines of the file are read and returned as a
        list. No end of line characters are stripped. If EOF is
        encountered immediately an empty list is returned.


        Preconditions:

        * The file is already open with a text read mode.


        Postconditions:

        * The rest of the file is read into a list of lines and
          returned.

        """
        raise NotImplementedError


    def write(self,s):
        """
        Writes the string s to the file. Note that writing to a file
        may be buffered and therefore ``s`` may not show up in the
        file until the ``close`` method is called. TODO: add flush
        method.


        Preconditions:
        
        * The file is already open with a write mode.


        Postconditions:

        * The string s is written to the file.

        """
        raise NotImplementedError

    def writeLines(self,lines):
        """
        Writes a list of lines to the file. This method is meant to be
        the equivalent of the ``readLines`` method and therefore each
        line should end with the required end of line character(s). 


        Preconditions:

        * The file is already open with a text write mode.


        Postconditions:

        * The write method is called for each line in the list.

        """
        raise NotImplementedError

    def close(self):
        """
        Ensures that the file is closed. This method should check to
        see whether the file is open first before trying to close it.


        Preconditions:
         * None


        Postconditions:
         * The file is closed

        """
        raise NotImplementedError


    def getStat(self):
        """
        Returns a dict containing some informational fields about the
        file. Different implementations will have different fields but
        some common fields are:

        * size - the size of the file.
        * creationTime - the time that the file was created.
        * accessTime - the time that the file was last accessed.
        * modificationTime - the time that the file was last modified.


        Preconditions:

        * The file exists.


        Postconditions:
        
        * A dict is returned containing some implementation specific
          information.

        """
        raise NotImplementedError


    def getPath(self):
        """
        Returns a Path object for this file.


        Preconditions:

        * None
        

        Postconditions:

        * A Path object for this file's path is returned.

        """
        raise NotImplementedError


    """
    Methods to include later:
     * getSize()
     * getAccessTime()?
     * getModifiedTime()?
     * getCreationTime()?
     * rename()
     * copy()
     * move()
     * remove()
    
    """
