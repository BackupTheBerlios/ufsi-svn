import os
import os.path


class NativeFile(FileInterface):
	def __init__(self,path):
		self.path=path
		self.pathStr=str(path)
		self.fileHandle=None


	# =============================================
	# File info
	# =============================================
	def getPath(self):
		return self.path
		
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
		# TODO: should we also check that it's a file?
		os.path.exists(self.pathStr)



	# =============================================
	# Opening the file
	# =============================================
	def open(self,mode="r"):
		if not fileHandle: fileHandle=file(self.pathStr,mode)
	
	def close(self):
		if fileHandle: fileHandle.close()

	def read(self):
		return fileHandle.read()
		
	def readline(self):
		return fileHandle.readline()
	
	def readlines(self):
		return fileHandle.readlines()

	def write(self,s):
		fileHandle.write(s)
		
	def writelines(self,lines):
		fileHandle.writelines(lines)



	# =============================================
	# File system operations on the file
	# =============================================
	def chmod(self,mode):
		os.chmod(self.pathStr,mode)

	def chown(self,owner,group):
		"""
		"""
		raise NotImplementedError
		
	def renameFile(self,fileName):
		os.rename(self.pathStr,str(self.path.getParentDirPath().join(fileName)))

	def move(self,destPath,createDirs=false):
		rename=os.rename
		if createDirs: rename=os.renames
		rename(self.pathStr,str(destPath))

	def copy(self,destPath,createDirs=false):	
		"""
		"""
		raise NotImplementedError

	def remove(self):
		os.remove(self.pathStr)
