
import sys



class CPError(Exception):

    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return repr(self.type+":"+self.value)


class CPSocketError(CPError):

    def __init__(self,value):
        CPError.__init__(self,"SOCKET",value)

class CPSocketConnectError(CPError):

    def __init__(self,value):
        CPError.__init__(self,"SOCKET",value)

        
class CPXmlContentExcption(CPError):

    def __init__(self,value):
        CPError.__init__(self,"XMLContent",value)
