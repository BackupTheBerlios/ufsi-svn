import os
import os.path


class NativeDir(DirInterface):
	def __init__(self,path):
		self.path=path
		self.pathStr=str(path)


	# =============================================
	# File system info
	# =============================================
	def getPath(self):
		return self.path

	def getParentDir(self):
		self.path.getParentDirPath.getDir()
		
	def getAtime(self):
		os.path.getatime(self.pathStr)
	
	def getMtime(self):
		os.path.getmtime(self.pathStr)
	
	def getCtime(self):
		os.path.getctime(self.pathStr)
	
	def getSize(self):
		os.path.getsize(self.pathStr)

	def getStat(self):
		os.stat(self.pathStr)
		
	def exists(self):
		# TODO: should we also check that it's a dir?
		os.path.exists(self.pathStr)
		

	# =============================================
	# File system operations on the dir
	# =============================================
	def getDirList(self,pattern):
		# TODO: use the pattern. Should the pattern be unix style? or re style?
		return os.listdir(self.pathStr)

	def chmod(self,mode):
		"""
		"""
		raise NotImplementedError
		
	def chown(self,owner,group=None):
		"""
		"""
		raise NotImplementedError
		
	def mkdir(self,includeParentDirs=False):
		# TODO: handle unc paths
		# TODO: take a mode
		mk=os.mkdir
		if includeParentDirs: mk=os.makedirs
		mk(self.pathStr)

	def rename(self,dirName):
		"""
		"""
		raise NotImplementedError
		
	def move(self,destPath,mkDirs=False):
		"""
		"""
		raise NotImplementedError
		
	def copy(self,destPath,mkDirs=False):
		"""
		"""
		raise NotImplementedError
		
	def remove(self,includeContents=False):
		# TODO: remove contents
		os.removedirs(self.pathStr)
		
	
	# =============================================
	# Walk through the file system tree
	# =============================================
	def walkAll(self,function,topDown=False,followSymLinks=False):
		"""
		"""
		raise NotImplementedError
		
	def walkFiles(self,function,topDown=False,followSymLinks=False):
		"""
		"""
		raise NotImplementedError
		
	def walkDirs(self,function,topDown=False,followSymLinks=False):
		"""
		"""
		raise NotImplementedError
		
	
	