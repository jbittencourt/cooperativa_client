

from error import *




class COOPloginFailed(CPError):

    def __init__(self):
        CPError.__init__(self,"COOP","Login failed")


class COOPcenarioAcessDenied(CPError):

    def __init__(self):
        CPError.__init__(self,"COOP","Access to cenario denied.")

