"""
A Dir object provides an object oriented interface to dir related
functions that are performable on a dir.

The DirInterface class specifies the methods required on all Dir
objects. All Dir implementations must implement them and adhere to
their specifications.

"""


class DirInterface:
    """
    The DirInterface class cannot be instantiated as it is really just
    an interface definition. Each method's docstring contains the
    specification for that method.
    
    """
    
    def __init__(self,path):
        """
        Creates an instance of the Dir implementation given a Path
        object.


        Preconditions:

        * path is an instance of PathInstance


        Postconditions:

        * a Dir object is instantiated
        
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns the path to this dir (as a string, of course).


        Preconditions:

        * None


        Postconditions:

        * The path to the dir that this Dir object works on is
          returned.
        
        """
        raise NotImplementedError


    def getDirList(self,filter=None,sort=None):
        """
        Returns a list of Path objects that represent each file or
        directory contained within this directory. The ``filter``
        parameter should be a regular expression string used with the
        ``re`` module's ``match`` method. The ``sort`` parameter
        should be a string matching one of the dictionary items from a
        Path.split() method call.


        Preconditions:

        * The dir exists on the file system.


        Postconditions:

        * A list of Path objects are returned that represent the list
          of files and directories within this directory.

        """
        raise NotImplementedError


    def getStat(self):
        """
        Returns a dict containing some informational fields about the
        dir. Different implementations will have different fields but
        some common fields are listed in the FileInterface class's
        equivalent method.

        TODO: should the getStat method be present on the Path object,
        instead?


        Preconditions:

        * The dir exists


        Postconditions:

        * A dict is returned containing some implementation specific
          information.
        
        """
        raise NotImplementedError


    def getPath(self):
        """
        Returns a Path object for this directory.


        Preconditions:

        * None


        Postconditions:

        * A Path object for this dir's path is returned.
        
        """
        raise NotImplementedError


    """
    Methods to add later:
     * getSize()

     * walk()

     * chmod()
     * chown()

     * mkdir()
     * rmdir()
     * rename()
     * move()
     * copy()
     
    """
