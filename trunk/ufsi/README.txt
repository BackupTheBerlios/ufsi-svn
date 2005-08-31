Universal File System Interface

(C)opyRight 2005 Adam Kerz


Introduction
============

Ufsi defines a standard interface for providing access to various file
systems. It also contains various implementations of the interface.
This early release is far from complete, however it does support basic
operations that are commonly performed on a file system.

It has been developed in association with Google's Summer Of Code
competition, 2005. Much appreciation goes out to Google for giving me
this opportunity. Thank you.


Installation
============

Currently installation is a manual process of putting the ``src/ufsi``
directory and its contents into the site-packages directory of
python's lib directory.

Eg:
On Unix:

  /usr/local/lib/python2.4/site-packages

On Windows:

  C:\Python\lib\site-packages


(or by creating/modifying user.pth in those directories.)


A setup.py script is being worked on. When that is complete you will
simply need to run:

   ``python setup.py install``


Testing
=======

A substantial set of test cases has been compiled in the ``src/test``
directory. After installing the ufsi package, you will need to set up
the test data for an FTP server and an HTTP server. The data is found
in ``src/test/data``. Under that directory are the directories Ftp,
Http and Tar.

A tar file has already been created and saved in ``src/test/data`` but
you can recreate it by running create from the Tar directory.

You will need to copy the contents of the Http directory into your
server's root path, so that you can find ``http://server/existing``
and ``http://server/existingDir/`` with a web browser.

You will need to copy the contents of the Ftp directory into your
Ftp's root path, but under a directory called ``ufsiTd``. You will
also need to allow anonymous access to the server, as well as create
two new users ``ufsitestread`` (password: ``ufsitestread``), with read
access only, and ``ufsitestwrite`` (password: ``ufsitestwrite``), with
read and write access.

You will most likely have to change some settings in the test file,
especially the host names if you don't use localhost. You can also
change other settings if you want to place the files elsewhere. All
paths should be configured in the ``setUp()`` method of each
test class.

If you follow the above instructions and use localhost for both Ftp
and Http the tests should all work.

To run them use:

   ``python test.py``


It has been tested using IIS5 on a Win2K box for both FTP and HTTP and
Apache's httpd for HTTP and vsfptd for FTP on a Fedora Core 3 box. FTP
has also been tested on a Solairs 5.8 box, although I don't know what
FTP server was being used - presumably the default, whatever that may
be. Unfortunately the FTP protocol and resulting data from running the
exact same tests on all three FTP servers varied. If you get errors
from FTP don't be surprised.
