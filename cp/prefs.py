

import ConfigParser
import os


config = None

def loadPrefs(file):
    global config
    
    path = os.path.dirname(file)
    
    config = ConfigParser.ConfigParser()
    config.read(file)
    
    
    #set the relative path of prefs to a absolute one
    for option in config.options("paths"):
        val = path +"/"+ config.get("paths",option)
        config.set("paths",option,val)
        
    fontpath = config.get("paths","fonts")

    for option in config.options("fonts"):
        fontname = fontpath+"/"+config.get("fonts",option)
        config.set("fonts",option,fontname)
