import Url
import log4py
import os


_log=log4py.Logger().get_instance()


class LocalUrlBuilder(Url.UrlBuilderInterface):
	def isFileSystem(self,s):
		return True

	def build(self,s):
		return LocalUrl(s)


class LocalUrl(Url.UrlInterface):
	def __init__(self,s):
		self.__url=s
		self.__sep=(os.name=='nt' and '\\') or '/'
		if self.__sep=='\\': s.replace('/','\\')
		else: s.replace('\\','/')
		_log.debug('Created new LocalUrl (url: '+self.__url+')')
	
	def getSeparators(self):
		return (self.__sep,)

	def join(self,otherUrl):
		if issubclass(otherUrl.__class__,UrlInterface):
			sep=self.getSeparators()[0]
			otherUrlString=str(otherUrl)
			for sep in otherUrl.getSeparators():
				otherUrlString=str(otherUrlString).replace(sep,self.__sep)

			if not otherUrlString.startswith(self.__sep): otherUrlString=self.__sep+otherUrlString
			return LocalUrl(self.__url+otherUrlString)

		# always join with other Url objects only
		return self.join(Url.Url(otherUrl))


	def __str__(self):
		return self.__url

# LocalUrl is used by default, so we don't need to register ourselves
# Url.registerBuilder(LocalUrlBuilder())

