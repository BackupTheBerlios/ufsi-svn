import os,log4py


_log=log4py.Logger().get_instance()

builders=[]
def registerBuilder(b):
	builders.append(b)

def Url(s):
	for b in builders:
		_log.debug('Trying file system with builder: '+str(b.__class__))
		if b.isFileSystem(s):
			_log.debug('Found an appropriate builder')
			return b.build(s)
	return LocalUrl.LocalUrl(s)


class UrlBuilderInterface:
	def isFileSystem(self,s):
		raise NotImplementedError
	def build(self,s):
		raise NotImplementedError


class UrlInterface:
	def isDir(self):
		raise NotImplementedError
	def isFile(self):
		raise NotImplementedError
	def getSeparators(self):
		raise NotImplementedError
	def join(self,otherUrl):
		raise NotImplementedError
			

# import any known handlers, to allow them to register themselves
import LocalUrl
import HttpUrl
