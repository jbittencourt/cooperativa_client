import sys

import gamecontrol
import main_scr
import login_scr
import welcome_scr
import registry_scr

from events import *

class COOPgame(gamecontrol.CPgameControl):

    def __init__( self , evManager , autoLogin = False):
        gamecontrol.CPgameControl.__init__( self, evManager )
        
        self.guiClasses = { "game":  [main_scr.mainScreen],
                            "login": [login_scr.login],
                            "welcome": [welcome_scr.welcome],
                            "registry": [registry_scr.registryScreen]
                          }

        
        self.switchController("welcome")
        if  autoLogin:
          print "Auto-login activated"
          evManager.Post(TryLoginEvent("testuser","teste"))


    def Notify(self, event):

        if event==StartGameEvent:
            #change to game screen in screen/main_scr.py
            self.switchController("game")
            
            #listener implemented at cp/viewport.py
            self.evManager.Post(MainPlayerEvent(event.player_data))
            
        elif event==StartLoginEvent:
            self.switchController("login")
        elif event==StartRegistryEvent:
            self.switchController("registry")            
        elif event==StartWelcomeEvent:
            self.switchController("welcome")     
        elif event==LoginSuccessEvent:
            self.evManager.Post( StartGameEvent(event.user_data) )       
        else:
            gamecontrol.CPgameControl.Notify(self,event)

