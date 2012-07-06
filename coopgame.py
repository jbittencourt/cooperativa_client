import sys

import gamecontrol
import main_scr
import login_scr
import welcome_scr
import registry_scr

from events import *

class COOPgame(gamecontrol.CPgameControl):

    def __init__( self , evManager ):
        gamecontrol.CPgameControl.__init__( self, evManager )
        
        self.guiClasses = { "game":  [main_scr.mainScreen],
                            "login": [login_scr.login],
                            "welcome": [welcome_scr.welcome],
                            "registry": [registry_scr.registryScreen]
                          }

        self.switchController("welcome")

    def Notify(self, event):

        if event==StartGameEvent:
            self.switchController("game")
            self.evManager.Post(MainPlayerEvent(event.player_data))
        elif event==StartLoginEvent:
            self.switchController("login")
        elif event==StartRegistryEvent:
            self.switchController("registry")            
        elif event==StartWelcomeEvent:
            self.switchController("welcome")            
        else:
            gamecontrol.CPgameControl.Notify(self,event)

