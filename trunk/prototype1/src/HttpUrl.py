import Url,log4py

_log=log4py.Logger().get_instance()


class HttpUrlBuilder(Url.UrlBuilderInterface):
	def isFileSystem(self,s):
		if str(s).startswith('http://'):
			return True
		return False

	def build(self,s):
		return HttpUrl(s)


class HttpUrl(Url.UrlInterface):
	def __init__(self,s):
		self.__url=s
		_log.debug('Created new HttpUrl (url: '+self.__url+')')

	def getSeparators(self):
		return ('/',)

	def join(self,otherUrl):
		if issubclass(otherUrl.__class__,Url.UrlInterface):
			otherUrlString=str(otherUrl)
			for sep in otherUrl.getSeparators():
				otherUrlString=str(otherUrlString).replace(sep,'/')

			if not otherUrlString.startswith('/'): otherUrlString='/'+otherUrlString
			return HttpUrl(self.__url+otherUrlString)

		# always join with other Url objects only
		return self.join(Url.Url(otherUrl))


	def __str__(self):
		return self.__url

Url.registerBuilder(HttpUrlBuilder())
