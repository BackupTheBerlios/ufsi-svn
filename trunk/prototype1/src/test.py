import log4py
import Url
import HttpUrl

_log=log4py.Logger().get_instance()
_log.set_loglevel(log4py.LOGLEVEL_DEBUG)
_log.set_target(log4py.TARGET_SYS_STDOUT)


u=Url.Url('http://www.google.com')
u=u.join('helkp\\me.html')
_log.debug(str(u))
