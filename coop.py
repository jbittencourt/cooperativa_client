import sys, os

path = os.path.dirname( os.path.abspath( sys.argv[0] ) )
sys.path.append(path)
sys.path.append(path+"/cp/")
sys.path.append(path+"/screens/")


#Import Modules
import os, pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

import signal

import eventmanager
from events import *
import controllers
import coopgame
import coopxml
import soundcontrol

import prefs


def cancelHandler(signum, parm):
    print "Programa Abortado"
    os._exit(1)



def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    #Initialize Everything
    global path
    
    evManager = eventmanager.EventManager()
    
    prefs.loadPrefs(path+"/coop.ini")  
    
    signal.signal(signal.SIGINT, cancelHandler)
    
    spinner = controllers.CPUSpinnerController( evManager )
    comunication = coopxml.COOPcommunication( evManager )
    sound = soundcontrol.soundControl( evManager )
    control = coopgame.COOPgame( evManager )

    comunication.start()
    
    
    try:
        spinner.Run()
    except NotImplementedError, msg:
        text = "Not Implemented: "+ str(msg)
        ev = ExceptionEvent( text )
        evManager.Post( ev )
        

    evManager.flushEvents()
    os._exit(1)
    
if __name__ == '__main__':
    main()
