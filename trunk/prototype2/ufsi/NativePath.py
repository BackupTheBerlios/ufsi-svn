import os,os.path,re
import Path


__all__=['OS_TYPE',
		'FILE_SYSTEM_TYPE__NATIVE_UNIX',
		'FILE_SYSTEM_TYPE__NATIVE_WINDOWS',
		'FILE_SYSTEM_TYPE__NATIVE_UNC',
		'NativePathBuilder',
		'NativeWindowsPath',
		'NativeUnixPath']


# Are we on a unix based os or a windows based os
OS_TYPE__UNIX='unix'
OS_TYPE__WINDOWS='windows'

OS_TYPE=OS_TYPE__UNIX
if os.name=='nt':
	OS_TYPE=OS_TYPE__WINDOWS

# Constants for different file system types
FILE_SYSTEM_TYPE__NATIVE_UNIX='NativeUnix'
FILE_SYSTEM_TYPE__NATIVE_WINDOWS='NativeWindows'
FILE_SYSTEM_TYPE__NATIVE_UNC='NativeUNC'


class NativePathBuilder(Path.BuilderInterface):
	def isValidPath(self,s):
		"""
		Matches all paths. A local path is the default path
		"""
		return True

	def build(self,s):
		"""
		Creates a LocalPath object.
		"""
		#print OS_TYPE
		if OS_TYPE=='unix':
			return NativeUnixPath(s)
		elif OS_TYPE=='windows':
			return NativeWindowsPath(s)
		#return LocalPath(s)

Path.Builders.registerDefault(NativePathBuilder())


class AbstractNativePath(Path.PathInterface):
	def __init__(self,path):
		self.path=path

	def __str__(self):
		return self.path


	def isDir(self):
		return os.path.isdir(self.path)
	
	def isFile(self):
		return os.path.isfile(self.path)

	def isSymlink(self):
		return os.path.issymlink(self.path)


	def isRelative(self):
		return not self.isAbsolute()


	def getDir(self):
		pass
	
	def getFile(self):
		pass


	def join(self,path):
		"""
		This was written to be generic enough to work with any local path.
		"""
		if not isinstance(path,Path.PathInterface):
			path=Path.Path(path)
			#if path==None:
				# TODO: determine error heirarchy
				# raise 

		if path.isAbsolute():
			return path
		else:
			pathStr=str(path)
			# strip any starting separator strings
			while pathStr.startswith(path.getSeparator()):
				pathStr==pathStr[len(path.getSeparator()):]
			# convert paths separator string to our separator string
			pathStr=pathStr.replace(path.getSeparator(),self.getSeparator())
			# make sure we correctly insert a separator string
			if not self.path.endswith(self.getSeparator()):
				pathStr=self.getSeparator()+pathStr
			
			return self.__class__(self.path+pathStr)

	
	def getFileSystemType(self):
		return self.split()[0]

	def getHost(self):
		return self.split()[1]
	
	def getPort(self):
		return self.split()[2]
		
	def getDirsList(self):
		return self.split()[3]
		
	def getDirsString(self):
		return self._dirListToDirString(self.getDirsList())

	def getFileName(self):
		fileBase=self.getFileBase()
		fileExt=self.getFileExt()
		
		if fileExt==None: return fileBase
		return fileBase+"."+fileExt

	def getFileBase(self):
		return self.split()[4]
		
	def getFileExt(self):
		return self.split()[5]
		
	def _dirListToDirString(self,dirs):
		return ''.join([d+self.getSeparator() for d in dirs])
		

class NativeUnixPath(AbstractNativePath):
	def split(self):
		fsType=FILE_SYSTEM_TYPE__NATIVE_UNIX
		host=None
		port=None
		dirs=[]
		fileBase=None
		fileExt=None

		# split into dirs,filename
		parts=self.path.split(self.getSeparator())
		
		# the last part is a filename
		fileParts=parts[-1].rsplit('.',1)
		# extension or not, part 0 is the fileBase
		fileBase=fileParts[0]
		# but here we also have an extension
		if len(fileParts)==2: fileExt=fileParts[1]
		
		# we also had dirs
		if len(parts)>1:
			dirs=parts[:-1]
		
		return (fsType,host,port,dirs,fileBase,fileExt)


	def getParentDirPath(self):
		dirs=self.getDirsList()
		fileName=self.getFileName()

		# if it's a relative path and no dirs found,
		# or it's an absolute path but only the '' dir (ie. '/' path) and no fileName
		if len(dirs)==0 or (len(dirs)==1 and dirs[0]=='' and fileName==''):
			# then it has no parent dir
			return None

		# if our path is already pointing to a directory, get the dir's parent dir
		if self.getFileName()=='':
			dirs=dirs[:-1]

		return NativeUnixPath(self._dirListToDirString(dirs))


	def getSeparator(self):
		return '/'

	

	def isAbsolute(self):
		absolute=False
		# starts with a slash
		if self.path.startswith(self.getSeparator()): absolute=True
		# starts with a home directory
		if self.path.startswith('~'): absolute=True
		
		return absolute







class NativeWindowsPath(AbstractNativePath):
	def __init__(self,path):
		# convert forward slashes to back slashes 
		path=path.replace('/','\\')
		# TODO: work out why super doesn't work here
		AbstractNativePath.__init__(self,path)
		
	def split(self):
		fsType=FILE_SYSTEM_TYPE__NATIVE_WINDOWS
		host=None
		port=None
		dirs=[]
		fileBase=None
		fileExt=None

		path=self.path
		if NativeWindowsPath.__isUnc(path):
			# Unc is of the format \\server[.com]\dir\filename.ext
			fsType=FILE_SYSTEM_TYPE__NATIVE_UNC
			dirsStart=path.find('\\',2)
			if dirsStart==-1: dirsStart=len(path)
			host=path[2:dirsStart]
			path=path[dirsStart:]
		
		if NativeWindowsPath.__isDriveBased(path):
			# remove the drive letter
			path=path[2:]

		parts=path.split(self.getSeparator())
		
		# the last part is a filename
		fileParts=parts[-1].rsplit('.',1)
		# extension or not, part 0 is the fileBase
		fileBase=fileParts[0]
		# but here we also have an extension
		if len(fileParts)==2: fileExt=fileParts[1]
		
		# we also had dirs
		if len(parts)>1:
			dirs=parts[:-1]
		
		return (fsType,host,port,dirs,fileBase,fileExt)


	def getParentDirPath(self):
		raise NotImplementedError
		# TODO: Code this for windows
		dirs=self.getDirsList()
		fileName=self.getFileName()

		# if it's a relative path and no dirs found,
		# or it's an absolute path but only the '' dir (ie. '/' path) and no fileName
		if len(dirs)==0 or (len(dirs)==1 and dirs[0]=='' and fileName==''):
			# then it has no parent dir
			return None

		# if our path is already pointing to a directory, get the dir's parent dir
		if self.getFileName()=='':
			dirs=dirs[:-1]

		return NativeWindowsPath(self._dirListToDirString(dirs))


	# windows fs type only
	def getDriveLetter(self):
		if NativeWindowsPath.__isDriveBased(self.path): return self.path[0]
		return None


	def getSeparator(self):
		return '\\'
	
	
	def isAbsolute(self):
		absolute=False
		# starts with a slash
		if self.path.startswith(self.getSeparator()): absolute=True
		# starts with a home directory
		if self.path.startswith('~'): absolute=True
		
		# starts with a drive letter
		#if re.match('[a-zA-Z]:',self.path): absolute=True
		if NativeWindowsPath.__isDriveBased(self.path): absolute=True
		
		# is a unc path (this is really covered above)
		#if self.path.startswith(r'\\'): absolute=True
		if NativeWindowsPath.__isUnc(self.path): absolute=True

		return absolute


	@staticmethod
	def __isUnc(path):
		if path.startswith('\\'+'\\'): return True
		return False

	@staticmethod
	def __isDriveBased(path):
		if re.match('[a-zA-Z]:',path): return True
		return False

