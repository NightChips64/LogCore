import logcore.main as log

logger=log.MainLogger()

class a:
	a1="a1"
	_a2="_a2"
	__a3="__a3"
	def __init__(self):
		self.a4="a4"
		self._a5="_a5"
		self.__a6="__a6"

b=a()
logger.log_object(b)
