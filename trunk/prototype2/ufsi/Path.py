


class Builders:
	__builders=[]
	__defaultBuilder=None

	@classmethod
	def register(cls,b):
		cls.__builders.append(b)

	@classmethod
	def registerDefault(cls,b):
		cls.__defaultBuilder=b
	
	@classmethod
	def getBuilders(cls):
		return cls.__builders
	
	@classmethod
	def getDefaultBuilder(cls):
		return cls.__defaultBuilder



def Path(s):
	for b in Builders.getBuilders():
		if b.isValidPath(s):
			return b.build(s)
	
	defaultBuilder=Builders.getDefaultBuilder()
	if defaultBuilder!=None: return defaultBuilder.build(s)
	else: return None



class BuilderInterface:
	def isValidPath(self,s):
		"""
		Tests to see whether the string s contains a valid path for this builder.
		Pre: true
		Post:
		  s is a valid path for this builder and return value is true
		    or
		  s is not a valid path for this builder and return value is false.
		"""
		raise NotImplementedError

	def build(self,s):
		"""
		Creates an appropriate Path object and return it.
		Pre: self.isValidPath(s)
		Post: a Path object is returned
		"""
		raise NotImplementedError



class PathInterface:
	def __init__(self,path):
		raise NotImplementedError

	# -------------
	# Operator methods
	# -------------
	def __str__(self):
		raise NotImplementedError


	# -------------
	# Standard methods
	# -------------
	def join(self,path):
		"""
		Takes a Path object or a string and adds it to the end of this Path; returns a new Path object.
		"""
		raise NotImplementedError

	def split(self):
		"""
		<p>Splits this path into a tuple of (FSType, host, portNumber, [dirs], fileBase, fileExt]).</p>
		
		<ul>
			<li>FSType is the protocol name for any url style file systems, or:
				<ul>
					<li>NativeUNC - for a Windows Universal Naming Convention</li>
					<li>NativeUnix - for a regular path name</li>
					<li>NativeWindows - for a regular path name</li>
				</ul>
				TODO: Maybe this should be changed to Native with a subtype of unc, unix or windows?
			</li>
			<li>Host is a string that references the host or None if not given/applicable. It may be a host
				name or an ip address or an identifier from any other scheme.<br/>
				Eg. 'Hyde' from the UNC path '\\Hyde\'.</li>
			<li>Port number is an integer if provided or None if not given/applicable.<br/>
				Eg. for <code>http://www.example.com/dir/file</code> the port number is None.</li>
			<li>The list of dirs is a list of the strings that occur between the separator characters.<br/>
				Eg. for <code>/dir/file</code> the list of dirs is ['','dir'] but with <code>relative/dir/file</code>
				the list of dirs is ['relative','dir'].</li>
			<li>fileBase is anything before the last period or the end of the string but after the last separator character.</li>
			<li>fileExt is the string of anything after the last period (which is after the fileBase). If no period is present fileExt is None.</li>
		</ul>
		"""
		raise NotImplementedError

	def getParentDirPath(self):
		"""
		<p>Returns a path object referencing the parent directory of the directory or file that this
		path references.</p>
		
		<ul>
			<li>A file's parent directory is the directory that contains it:<br/>
				eg. 'dir/file' has a parent directory of 'dir/'.</li>
			<li>A dir's parent directory is the directory that contains it:<br/>
				eg. 'dir1/dir2/' has a parent directory of 'dir1'.</li>
			<li>The path '' is a valid directory path. It is a relative path that
				points to the current working directory.<br/>
				eg. 'dir/' has a parent directory of '', and 'file' also has a parent directory of ''.</li>
			<li>Naturally the path '/' doesn't have a parent directory and should instead return None.
				This is the case for any absolute path. Eg. 'http://www.example.com/' doesn't have a
				parent directory.</li>
		</ul>
		"""
		raise NotImplementedError
	
	def getFileSystemType(self):
		"""
		Constant representing the file system type of this path.
		"""
		raise NotImplementedError

	def getHost(self):
		"""
		Returns the host, or None if not applicable.
		"""
		raise NotImplementedError
	
	def getPort(self):
		"""
		Returns the port number specified in the path or None if no port number was given.
		"""
		raise NotImplementedError
		
	def getDirsList(self):
		"""
		Returns a list of dir name strings that this path is made up of. If the path starts with a
		separator character, the first dir is an empty string.
		"""
		raise NotImplementedError
		
	def getDirsString(self):
		"""
		Returns the dirs as a string.
		"""
		raise NotImplementedError

	def getFileName(self):
		"""
		Returns the file name (anything after the last separator character of this path) as a string.
		"""
		raise NotImplementedError

	def getFileBase(self):
		"""
		Returns the file base, which is everything in the fileName before the last '.'
		"""
		raise NotImplementedError
		
	def getFileExt(self):
		"""
		Returns anything after the last '.' in the fileName or None if there is no '.' in the fileName.
		"""
		raise NotImplementedError


	def getSeparator(self):
		"""
		Returns the separator string for this path type.
		"""
		raise NotImplementedError


	def isDir(self):
		"""
		Tests whether this Path object refers to a directory on the target File System.
		"""
		raise NotImplementedError

	def isFile(self):
		"""
		Tests whether this Path object refers to a file on the target File System.
		"""
		raise NotImplementedError

	def isSymlink(self):
		"""
		Tests whether this Path object refers to a symlink on the target File System.
		"""
		raise NotImplementedError


	def isRelative(self):
		"""
		Returns true if the path is relative to the current working directory.
		"""
		raise NotImplementedError
		
	def isAbsolute(self):
		"""
		Returns true if the path is not relative to the current working directory.
		"""
		raise NotImplementedError


	def getDir(self):
		"""
		Returns a Dir object to manipulate the dir referenced by this Path.
		Pre: self.isDir()
		Post: returns a Dir object
		"""
		raise NotImplementedError

	def getFile(self):
		"""
		Returns a File object to manipulate the file referenced by this Path.
		Pre: self.isFile()
		Post: returns a File object
		"""
		raise NotImplementedError


