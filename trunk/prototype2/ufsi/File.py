

class FileInterface:
	def __init__(self,path):
		"""
		"""
		raise NotImplementedError



	# =============================================
	# File info
	# =============================================
	def getPath(self):
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
	# Opening the file
	# =============================================
	def open(self,mode):
		"""
		"""
		raise NotImplementedError
	
	def close(self):
		"""
		"""
		raise NotImplementedError

	def read(self):
		"""
		"""
		raise NotImplementedError
		
	def readline(self):
		"""
		"""
		raise NotImplementedError
	
	def readlines(self):
		"""
		"""
		raise NotImplementedError

	def write(self,s):
		"""
		"""
		raise NotImplementedError
		
	def writelines(self,lines):
		"""
		"""
		raise NotImplementedError



	# =============================================
	# File system operations on the file
	# =============================================
	def chmod(self,mode):
		"""
		TODO: are these (+chown) generic enough?ftp, unix, (windows?)
		"""
		raise NotImplementedError

	def chown(self,owner,group=None):
		"""
		"""
		raise NotImplementedError
		
	def renameFile(self,fileName):
		"""
		"""
		raise NotImplementedError

	def move(self,destPath,createDirs=False):
		"""
		"""
		raise NotImplementedError

	def copy(self,destPath,createDirs=False):	
		"""
		"""
		raise NotImplementedError

	def remove(self):
		"""
		"""
		raise NotImplementedError

