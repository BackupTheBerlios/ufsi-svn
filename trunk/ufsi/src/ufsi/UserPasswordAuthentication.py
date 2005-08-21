"""
A UserPasswordAuthentication object should be used by any
implementation that requires a (user, password) pair to gain access to
a file system.
"""

import ufsi

class UserPasswordAuthentication(ufsi.AuthenticationInterface):
    """
    The UserPasswordAuthentication class stores a user and password
    pair for use by a ufsi implementation to authenticate a request.
    """
    
    def __init__(self,user,password):
        """
        Construct a UserPasswordAuthentication instance with the given
        user and password.

        Both parameters are required, however a value of ``None`` for
       	password indicates that no password is required (for
       	authentication), whereas an empty string ('') indicates that a
       	password is required and it is the empty string. All file
       	system implementations where this is applicable must make this
       	distinction.
       	"""
        self.__user=user
        self.__password=password


    def getUser(self):
        """
        Returns the user.
        """
        return self.__user

    def getPassword(self):
        """
        Returns the password.
        """
        return self.__password

