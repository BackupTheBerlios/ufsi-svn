

class DirInterface:
	def __init__(self,path):
		"""
		"""
		raise NotImplementedError

		
	# =============================================
	# File system info
	# =============================================
	def getPath(self):
		"""
		"""
		raise NotImplementedError

	def getParentDir(self):
		"""
		"""
		raise NotImplementedError
		
	def getAtime(self):
		"""
		"""
		raise NotImplementedError
		
	def getMtime(self):
		"""
		"""
		raise NotImplementedError
		
	def getCtime(self):
		"""
		"""
		raise NotImplementedError
		
	def getSize(self):
		"""
		"""
		raise NotImplementedError
		
	def getStat(self):
		"""
		"""
		raise NotImplementedError
		
	def exists(self):
		"""
		"""
		raise NotImplementedError
		

	# =============================================
	# File system operations on the dir
	# =============================================
	def getDirList(self,pattern):
		"""
		"""
		raise NotImplementedError

	def chmod(self,mode):
		"""
		"""
		raise NotImplementedError
		
	def chown(self,owner,group=None):
		"""
		"""
		raise NotImplementedError
		
	def mkdir(self,includeParentDirs=False):
		"""
		"""
		raise NotImplementedError
		
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
		"""
		"""
		raise NotImplementedError
		
	
	# =============================================
	# Walk through the file system tree
	# =============================================
	# TODO: change this to reflect normal os.walk functionality - hint: os functions are decent and accepted as good - replicate on other fs
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
		
	
	