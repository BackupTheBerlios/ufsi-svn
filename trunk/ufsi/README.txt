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


License
=======

Ufsi is distributed under the MIT License. You will find it in the file
'License.txt' in the root of this repository.


Installation
============

Simply execute the ``setup.py`` script found in the ``src/`` directory
like so:

   ``python setup.py install``


Usage
=====

The ufsi is mainly comprised of three interface definitions:

* Path (defined in PathInterface)
* File (defined in FileInterface)
* Dir (defined in DirInterface)

Ufsi currently supports FTP, HTTP, Native (anything the os module
supports) and TAR file systems.

An example of how to use ufsi is:

  import ufsi

  p=ufsi.Path('/etc/hosts')
  assert p.isFile()
  f=p.getFile()
  f.open('r')
  print f.read(20)
  print f.readLines()
  f.close()


To use ufsi with an HTTP file, simply replace '/etc/hosts' with
'http://www.google.com.au' in the above example.


To use ufsi with an FTP file, replace the url as above, but you may
also need to setup the authentication parameters for the connection.
You can do this like so:

  auth=ufsi.UserPasswordAuthentication('username','password')
  ftpPath.setAuthentication(auth)

The you can proceed to perform operations on an FTP file system as
that user.


To use ufsi with a TAR file you must explicitly create a TAR Path
object, after which all normal operations are available:

  tarFilePath=ufsi.Path('/tmp/tarfile.tar')
  tarPath=ufsi.TarPath(tarFilePath,'dir/file')

This creates a path to 'dir/file' in the TAR file.


For complete information on the interface definitions see the file
UFSIDEFINITION.txt. For information specific to a certain
implementation, you will currently have to read the docstrings in the
source code.


Note: HTTP is a read only protocol and also doesn't have a concept of
directories. It has a heirarchy path to access a file, but no
directory list. Instead a path like 'http://www.google.com.au/' is
considered a file.


Note: TAR support is currently read only as python's tarfile module,
and TAR files themselves aren't set up write support. It may be
possible, and infact many operations are, but more investigation needs
to be performed before implementing this.


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
